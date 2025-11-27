#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/11/18
# @USER    : Shengji He
# @File    : notification.py
# @Software: PyCharm
# @Version  : Python-
# @TASK:
from typing import Dict, List, Tuple, Optional, Union
import time
from utils import get_beijing_time, strip_markdown, clean_title
import requests


def format_rank_display(ranks: List[int], format_type: str) -> str:
    """统一的排名格式化方法"""
    if not ranks:
        return ""

    star, new_star = ranks

    if format_type == "html":
        highlight_start = "<font color='red'><strong>"
        highlight_end = "</strong></font>"
    elif format_type == "feishu":
        highlight_start = "<font color='red'>**"
        highlight_end = "**</font>"
    elif format_type == "dingtalk":
        highlight_start = "**"
        highlight_end = "**"
    elif format_type == "wework":
        highlight_start = "**"
        highlight_end = "**"
    elif format_type == "telegram":
        highlight_start = "<b>"
        highlight_end = "</b>"
    else:
        highlight_start = "**"
        highlight_end = "**"

    if star >= 10000 or new_star >= 1000:
        return f"{highlight_start}[star: {star}]{highlight_end}"
    else:
        return f"[star: {star}]"


def format_title_for_platform(platform: str, title_data) -> str:
    """统一的标题格式化方法"""
    title, link_url, description, star, fork, new_star = title_data[:6]
    is_new = False  # TODO: add tag
    if len(title_data) == 7:
        is_new = title_data[6]

    rank_display = format_rank_display([star, new_star], platform)

    cleaned_title = clean_title(title)

    if platform == "feishu":
        if link_url:
            formatted_title = f"[{cleaned_title}]({link_url})"
        else:
            formatted_title = cleaned_title

        title_prefix = "🆕 " if is_new else ""

        result = f"{title_prefix}{formatted_title}"

        if rank_display:
            result += f" {rank_display}"
        if fork > 0:
            result += f" <font color='grey'>- Fork: {fork}</font>"
        if new_star > 0:
            result += f" <font color='green'>(Today stars: {new_star}次)</font>"
        if description:
            result += f"\n    {description}"
        return result

    elif platform == "dingtalk":
        if link_url:
            formatted_title = f"[{cleaned_title}]({link_url})"
        else:
            formatted_title = cleaned_title

        title_prefix = "🆕 " if is_new else ""

        result = f"{title_prefix}{formatted_title}"

        if rank_display:
            result += f" {rank_display}"
        if fork > 0:
            result += f" `- Fork: {fork}`"
        if new_star > 0:
            result += f" `(Today stars: {new_star}次)`"
        if description:
            result += f"\n    {description}"

        return result

    elif platform == "wework":
        if link_url:
            formatted_title = f"[{cleaned_title}]({link_url})"
        else:
            formatted_title = cleaned_title

        title_prefix = "🆕 " if is_new else ""

        result = f"{title_prefix}{formatted_title}"

        if rank_display:
            result += f" {rank_display}"
        if fork > 0:
            result += f" `- Fork: {fork}`"
        if new_star > 0:
            result += f" `(Today stars: {new_star}次)`"
        if description:
            result += f"\n    {description}"

        return result

    # elif platform == "telegram":
    #     if link_url:
    #         formatted_title = f'<a href="{link_url}">{html_escape(cleaned_title)}</a>'
    #     else:
    #         formatted_title = cleaned_title
    #
    #     title_prefix = "🆕 " if is_new else ""
    #
    #     if show_source:
    #         result = f"[{title_data['source_name']}] {title_prefix}{formatted_title}"
    #     else:
    #         result = f"{title_prefix}{formatted_title}"
    #
    #     if rank_display:
    #         result += f" {rank_display}"
    #     if title_data["time_display"]:
    #         result += f" <code>- {title_data['time_display']}</code>"
    #     if title_data["count"] > 1:
    #         result += f" <code>({title_data['count']}次)</code>"
    #
    #     return result

    elif platform == "ntfy":
        if link_url:
            formatted_title = f"[{cleaned_title}]({link_url})"
        else:
            formatted_title = cleaned_title

        title_prefix = "🆕 " if is_new else ""

        result = f"{title_prefix}{formatted_title}"

        if rank_display:
            result += f" {rank_display}"
        if fork > 0:
            result += f" `- Fork: {fork}`"
        if new_star > 0:
            result += f" `(Today stars: {new_star}次)`"
        if description:
            result += f"\n    {description}"
        return result

    # elif platform == "html":
    #     rank_display = format_rank_display(
    #         title_data["ranks"], title_data["rank_threshold"], "html"
    #     )
    #
    #     link_url = title_data["mobile_url"] or title_data["url"]
    #
    #     escaped_title = html_escape(cleaned_title)
    #     escaped_source_name = html_escape(title_data["source_name"])
    #
    #     if link_url:
    #         escaped_url = html_escape(link_url)
    #         formatted_title = f'[{escaped_source_name}] <a href="{escaped_url}" target="_blank" class="news-link">{escaped_title}</a>'
    #     else:
    #         formatted_title = (
    #             f'[{escaped_source_name}] <span class="no-link">{escaped_title}</span>'
    #         )
    #
    #     if rank_display:
    #         formatted_title += f" {rank_display}"
    #     if title_data["time_display"]:
    #         escaped_time = html_escape(title_data["time_display"])
    #         formatted_title += f" <font color='grey'>- {escaped_time}</font>"
    #     if title_data["count"] > 1:
    #         formatted_title += f" <font color='green'>({title_data['count']}次)</font>"
    #
    #     if is_new:
    #         formatted_title = f"<div class='new-title'>🆕 {formatted_title}</div>"
    #
    #     return formatted_title

    else:
        return cleaned_title


def split_content_into_batches(
        report_data: Dict,
        format_type: str,
        languages: List[str],
        update_info: Optional[Dict] = None,
        max_bytes: int = None,
        CONFIG=None,
) -> List[str]:
    """分批处理消息内容，确保词组标题+至少第一条新闻的完整性"""
    if max_bytes is None:
        if format_type == "dingtalk":
            max_bytes = CONFIG.get("DINGTALK_BATCH_SIZE", 20000)
        elif format_type == "feishu":
            max_bytes = CONFIG.get("FEISHU_BATCH_SIZE", 29000)
        elif format_type == "ntfy":
            max_bytes = 3800
        else:
            max_bytes = CONFIG.get("MESSAGE_BATCH_SIZE", 4000)

    batches = []

    total_titles = sum(len(stat) for stat in report_data.values())
    now = get_beijing_time()

    base_header = ""
    if format_type == "wework":
        base_header = f"**总数：** {total_titles}\n\n\n\n"
    elif format_type == "telegram":
        base_header = f"总数： {total_titles}\n\n"
    elif format_type == "ntfy":
        base_header = f"**总数：** {total_titles}\n\n"
    elif format_type == "feishu":
        base_header = ""
    elif format_type == "dingtalk":
        base_header = f"**总数：** {total_titles}\n\n"
        base_header += f"**时间：** {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        base_header += f"**类型：** 热点分析报告\n\n"
        base_header += "---\n\n"

    base_footer = ""
    if format_type == "wework":
        base_footer = f"\n\n\n> 更新时间：{now.strftime('%Y-%m-%d %H:%M:%S')}"
        if update_info:
            base_footer += f"\n> TrendRadar 发现新版本 **{update_info['remote_version']}**，当前 **{update_info['current_version']}**"
    elif format_type == "telegram":
        base_footer = f"\n\n更新时间：{now.strftime('%Y-%m-%d %H:%M:%S')}"
        if update_info:
            base_footer += f"\nTrendRadar 发现新版本 {update_info['remote_version']}，当前 {update_info['current_version']}"
    elif format_type == "ntfy":
        base_footer = f"\n\n> 更新时间：{now.strftime('%Y-%m-%d %H:%M:%S')}"
        if update_info:
            base_footer += f"\n> TrendRadar 发现新版本 **{update_info['remote_version']}**，当前 **{update_info['current_version']}**"
    elif format_type == "feishu":
        base_footer = f"\n\n<font color='grey'>更新时间：{now.strftime('%Y-%m-%d %H:%M:%S')}</font>"
        if update_info:
            base_footer += f"\n<font color='grey'>TrendRadar 发现新版本 {update_info['remote_version']}，当前 {update_info['current_version']}</font>"
    elif format_type == "dingtalk":
        base_footer = f"\n\n> 更新时间：{now.strftime('%Y-%m-%d %H:%M:%S')}"
        if update_info:
            base_footer += f"\n> TrendRadar 发现新版本 **{update_info['remote_version']}**，当前 **{update_info['current_version']}**"

    stats_header = ""
    # if format_type == "wework":
    #     stats_header = f"📊 **Github Trending**\n\n"
    # elif format_type == "telegram":
    #     stats_header = f"📊 Github Trending\n\n"
    # elif format_type == "ntfy":
    #     stats_header = f"📊 **Github Trending**\n\n"
    # elif format_type == "feishu":
    #     stats_header = f"📊 **Github Trending**\n\n"
    # elif format_type == "dingtalk":
    #     stats_header = f"📊 **Github Trending**\n\n"

    current_batch = base_header
    current_batch_has_content = False

    # 处理Github Trending
    if '' not in languages:
        cur_languages = [''] + languages
    else:
        cur_languages = languages

    total_count = len(cur_languages)

    # 添加统计标题
    test_content = current_batch + stats_header
    if len(test_content.encode("utf-8")) + len(base_footer.encode("utf-8")) < max_bytes:
        current_batch = test_content
        current_batch_has_content = True
    else:
        if current_batch_has_content:
            batches.append(current_batch + base_footer)
        current_batch = base_header + stats_header
        current_batch_has_content = True

    # 逐个处理词组（确保词组标题+第一条新闻的原子性）
    # 处理主要统计数据
    for i, cur_language in enumerate(cur_languages):
        all_lang = report_data.get(cur_language, [])
        if cur_language == '':
            cur_language = 'all'
        word = cur_language.capitalize()
        count = len(all_lang)
        sequence_display = f"[{i + 1}/{total_count}]"
        if count == 0:
            continue
        # 构建词组标题
        word_header = ""
        if format_type == "wework":
            if count >= 10:
                word_header = (
                    f"🔥 {sequence_display} **{word}** : **{count}** 条\n\n"
                )
            elif count >= 5:
                word_header = (
                    f"📈 {sequence_display} **{word}** : **{count}** 条\n\n"
                )
            else:
                word_header = f"📌 {sequence_display} **{word}** : {count} 条\n\n"
        elif format_type == "telegram":
            if count >= 10:
                word_header = f"🔥 {sequence_display} {word} : {count} 条\n\n"
            elif count >= 5:
                word_header = f"📈 {sequence_display} {word} : {count} 条\n\n"
            else:
                word_header = f"📌 {sequence_display} {word} : {count} 条\n\n"
        elif format_type == "ntfy":
            if count >= 10:
                word_header = (
                    f"🔥 {sequence_display} **{word}** : **{count}** 条\n\n"
                )
            elif count >= 5:
                word_header = (
                    f"📈 {sequence_display} **{word}** : **{count}** 条\n\n"
                )
            else:
                word_header = f"📌 {sequence_display} **{word}** : {count} 条\n\n"
        elif format_type == "feishu":
            if count >= 10:
                word_header = f"🔥 <font color='grey'>{sequence_display}</font> **{word}** : <font color='red'>{count}</font> 条\n\n"
            elif count >= 5:
                word_header = f"📈 <font color='grey'>{sequence_display}</font> **{word}** : <font color='orange'>{count}</font> 条\n\n"
            else:
                word_header = f"📌 <font color='grey'>{sequence_display}</font> **{word}** : {count} 条\n\n"
        elif format_type == "dingtalk":
            if count >= 10:
                word_header = (
                    f"🔥 {sequence_display} **{word}** : **{count}** 条\n\n"
                )
            elif count >= 5:
                word_header = (
                    f"📈 {sequence_display} **{word}** : **{count}** 条\n\n"
                )
            else:
                word_header = f"📌 {sequence_display} **{word}** : {count} 条\n\n"

        # 构建第一条新闻
        first_title_data = all_lang[0]
        first_news_line = ""
        if format_type == "wework":
            formatted_title = format_title_for_platform(
                "wework", first_title_data,
            )
        elif format_type == "telegram":
            formatted_title = format_title_for_platform(
                "telegram", first_title_data,
            )
        elif format_type == "ntfy":
            formatted_title = format_title_for_platform(
                "ntfy", first_title_data,
            )
        elif format_type == "feishu":
            formatted_title = format_title_for_platform(
                "feishu", first_title_data,
            )
        elif format_type == "dingtalk":
            formatted_title = format_title_for_platform(
                "dingtalk", first_title_data,
            )
        else:
            formatted_title = f"{first_title_data['title']}"

        first_news_line = f"  1. {formatted_title}\n"
        if count > 1:
            first_news_line += "\n"

        # 原子性检查：词组标题+第一条新闻必须一起处理
        word_with_first_news = word_header + first_news_line
        test_content = current_batch + word_with_first_news

        if (
                len(test_content.encode("utf-8")) + len(base_footer.encode("utf-8"))
                >= max_bytes
        ):
            # 当前批次容纳不下，开启新批次
            if current_batch_has_content:
                batches.append(current_batch + base_footer)
            current_batch = base_header + stats_header + word_with_first_news
            current_batch_has_content = True
            start_index = 1
        else:
            current_batch = test_content
            current_batch_has_content = True
            start_index = 1

        # 处理剩余新闻条目
        for j in range(start_index, count):
            title_data = all_lang[j]
            if format_type == "wework":
                formatted_title = format_title_for_platform(
                    "wework", title_data,
                )
            elif format_type == "telegram":
                formatted_title = format_title_for_platform(
                    "telegram", title_data,
                )
            elif format_type == "ntfy":
                formatted_title = format_title_for_platform(
                    "ntfy", title_data,
                )
            elif format_type == "feishu":
                formatted_title = format_title_for_platform(
                    "feishu", title_data,
                )
            elif format_type == "dingtalk":
                formatted_title = format_title_for_platform(
                    "dingtalk", title_data,
                )
            else:
                formatted_title = f"{title_data['title']}"

            news_line = f"  {j + 1}. {formatted_title}\n"
            if j < count - 1:
                news_line += "\n"

            test_content = current_batch + news_line
            if (
                    len(test_content.encode("utf-8")) + len(base_footer.encode("utf-8"))
                    >= max_bytes
            ):
                if current_batch_has_content:
                    batches.append(current_batch + base_footer)
                current_batch = base_header + stats_header + word_header + news_line
                current_batch_has_content = True
            else:
                current_batch = test_content
                current_batch_has_content = True

        # 词组间分隔符
        if i < total_count - 1:
            separator = ""
            if format_type == "wework":
                separator = f"\n\n\n\n"
            elif format_type == "telegram":
                separator = f"\n\n"
            elif format_type == "ntfy":
                separator = f"\n\n"
            elif format_type == "feishu":
                separator = f"\n{CONFIG['FEISHU_MESSAGE_SEPARATOR']}\n\n"
            elif format_type == "dingtalk":
                separator = f"\n---\n\n"

            test_content = current_batch + separator
            if (
                    len(test_content.encode("utf-8")) + len(base_footer.encode("utf-8"))
                    < max_bytes
            ):
                current_batch = test_content

    # 完成最后批次
    if current_batch_has_content:
        batches.append(current_batch + base_footer)

    return batches


def send_to_notifications(
        report_data: Dict,
        languages: List[str],
        report_type: str = "当日汇总",
        update_info: Optional[Dict] = None,
        proxy_url: Optional[str] = None,
        mode: str = "daily",
        html_file_path: Optional[str] = None,
        CONFIG=None,
) -> Dict[str, bool]:
    """发送数据到多个通知平台"""
    results = {}

    # if CONFIG["PUSH_WINDOW"]["ENABLED"]:
    #     push_manager = PushRecordManager()
    #     time_range_start = CONFIG["PUSH_WINDOW"]["TIME_RANGE"]["START"]
    #     time_range_end = CONFIG["PUSH_WINDOW"]["TIME_RANGE"]["END"]
    #
    #     if not push_manager.is_in_time_range(time_range_start, time_range_end):
    #         now = get_beijing_time()
    #         print(
    #             f"推送窗口控制：当前时间 {now.strftime('%H:%M')} 不在推送时间窗口 {time_range_start}-{time_range_end} 内，跳过推送"
    #         )
    #         return results
    #
    #     if CONFIG["PUSH_WINDOW"]["ONCE_PER_DAY"]:
    #         if push_manager.has_pushed_today():
    #             print(f"推送窗口控制：今天已推送过，跳过本次推送")
    #             return results
    #         else:
    #             print(f"推送窗口控制：今天首次推送")

    # report_data = prepare_report_data(stats, failed_ids, new_titles, id_to_name, mode)

    # feishu_url = CONFIG["FEISHU_WEBHOOK_URL"]
    # dingtalk_url = CONFIG["DINGTALK_WEBHOOK_URL"]
    # wework_url = CONFIG["WEWORK_WEBHOOK_URL"]
    # telegram_token = CONFIG["TELEGRAM_BOT_TOKEN"]
    # telegram_chat_id = CONFIG["TELEGRAM_CHAT_ID"]
    # email_from = CONFIG["EMAIL_FROM"]
    # email_password = CONFIG["EMAIL_PASSWORD"]
    # email_to = CONFIG["EMAIL_TO"]
    # email_smtp_server = CONFIG.get("EMAIL_SMTP_SERVER", "")
    # email_smtp_port = CONFIG.get("EMAIL_SMTP_PORT", "")
    ntfy_server_url = CONFIG["NTFY_SERVER_URL"]
    ntfy_topic = CONFIG["NTFY_TOPIC"]
    ntfy_token = CONFIG.get("NTFY_TOKEN", "")
    bark_url = CONFIG["BARK_URL"]

    # update_info_to_send = update_info if CONFIG["SHOW_VERSION_UPDATE"] else None
    update_info_to_send = None

    # # 发送到飞书
    # if feishu_url:
    #     results["feishu"] = send_to_feishu(
    #         feishu_url, report_data, report_type, update_info_to_send, proxy_url, mode
    #     )
    #
    # # 发送到钉钉
    # if dingtalk_url:
    #     results["dingtalk"] = send_to_dingtalk(
    #         dingtalk_url, report_data, report_type, update_info_to_send, proxy_url, mode
    #     )
    #
    # # 发送到企业微信
    # if wework_url:
    #     results["wework"] = send_to_wework(
    #         wework_url, report_data, report_type, update_info_to_send, proxy_url, mode
    #     )
    #
    # # 发送到 Telegram
    # if telegram_token and telegram_chat_id:
    #     results["telegram"] = send_to_telegram(
    #         telegram_token,
    #         telegram_chat_id,
    #         report_data,
    #         report_type,
    #         update_info_to_send,
    #         proxy_url,
    #         mode,
    #     )

    # 发送到 ntfy
    if ntfy_server_url and ntfy_topic:
        results["ntfy"] = send_to_ntfy(
            ntfy_server_url,
            ntfy_topic,
            ntfy_token,
            report_data,
            languages,
            report_type,
            update_info_to_send,
            proxy_url,
            mode,
        )

    # 发送到 Bark
    if bark_url:
        results["bark"] = send_to_bark(
            bark_url,
            report_data,
            languages,
            report_type,
            update_info_to_send,
            proxy_url,
            mode,
        )

    # # 发送邮件
    # if email_from and email_password and email_to:
    #     results["email"] = send_to_email(
    #         email_from,
    #         email_password,
    #         email_to,
    #         report_type,
    #         html_file_path,
    #         email_smtp_server,
    #         email_smtp_port,
    #     )

    if not results:
        print("未配置任何通知渠道，跳过通知发送")

    # # 如果成功发送了任何通知，且启用了每天只推一次，则记录推送
    # if (
    #     CONFIG["PUSH_WINDOW"]["ENABLED"]
    #     and CONFIG["PUSH_WINDOW"]["ONCE_PER_DAY"]
    #     and any(results.values())
    # ):
    #     push_manager = PushRecordManager()
    #     push_manager.record_push(report_type)

    return results


def send_to_ntfy(
        server_url: str,
        topic: str,
        token: Optional[str],
        report_data: Dict,
        languages: List[str],
        report_type: str,
        update_info: Optional[Dict] = None,
        proxy_url: Optional[str] = None,
        mode: str = "daily",
) -> bool:
    """发送到ntfy（支持分批发送，严格遵守4KB限制）"""
    # 避免 HTTP header 编码问题
    # report_type_en_map = {
    #     "当日汇总": "Daily Summary",
    #     "当前榜单汇总": "Current Ranking",
    #     "增量更新": "Incremental Update",
    #     "实时增量": "Realtime Incremental",
    #     "实时当前榜单": "Realtime Current Ranking",
    # }
    # report_type_en = report_type_en_map.get(report_type, "News Report")
    report_type_en = report_type  # 'Github Trending'

    headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "Markdown": "yes",
        "Title": report_type_en,
        "Priority": "default",
        "Tags": "news",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    # 构建完整URL，确保格式正确
    base_url = server_url.rstrip("/")
    if not base_url.startswith(("http://", "https://")):
        base_url = f"https://{base_url}"
    url = f"{base_url}/{topic}"

    proxies = None
    if proxy_url:
        proxies = {"http": proxy_url, "https": proxy_url}

    # 获取分批内容，使用ntfy专用的4KB限制
    batches = split_content_into_batches(
        report_data, "ntfy", languages, update_info, max_bytes=3800,
    )

    total_batches = len(batches)
    print(f"ntfy消息分为 {total_batches} 批次发送 [{report_type}]")

    # 反转批次顺序，使得在ntfy客户端显示时顺序正确
    # ntfy显示最新消息在上面，所以我们从最后一批开始推送
    reversed_batches = list(reversed(batches))

    print(f"ntfy将按反向顺序推送（最后批次先推送），确保客户端显示顺序正确")

    # 逐批发送（反向顺序）
    success_count = 0
    for idx, batch_content in enumerate(reversed_batches, 1):
        # 计算正确的批次编号（用户视角的编号）
        actual_batch_num = total_batches - idx + 1

        batch_size = len(batch_content.encode("utf-8"))
        print(
            f"发送ntfy第 {actual_batch_num}/{total_batches} 批次（推送顺序: {idx}/{total_batches}），大小：{batch_size} 字节 [{report_type}]"
        )

        # 检查消息大小，确保不超过4KB
        if batch_size > 4096:
            print(f"警告：ntfy第 {actual_batch_num} 批次消息过大（{batch_size} 字节），可能被拒绝")

        # 添加批次标识（使用正确的批次编号）
        current_headers = headers.copy()
        if total_batches > 1:
            batch_header = f"**[第 {actual_batch_num}/{total_batches} 批次]**\n\n"
            batch_content = batch_header + batch_content
            current_headers["Title"] = (
                f"{report_type_en} ({actual_batch_num}/{total_batches})"
            )

        try:
            response = requests.post(
                url,
                headers=current_headers,
                data=batch_content.encode("utf-8"),
                proxies=proxies,
                timeout=30,
            )

            if response.status_code == 200:
                print(f"ntfy第 {actual_batch_num}/{total_batches} 批次发送成功 [{report_type}]")
                success_count += 1
                if idx < total_batches:
                    # 公共服务器建议 2-3 秒，自托管可以更短
                    interval = 2 if "ntfy.sh" in server_url else 1
                    time.sleep(interval)
            elif response.status_code == 429:
                print(
                    f"ntfy第 {actual_batch_num}/{total_batches} 批次速率限制 [{report_type}]，等待后重试"
                )
                time.sleep(10)  # 等待10秒后重试
                # 重试一次
                retry_response = requests.post(
                    url,
                    headers=current_headers,
                    data=batch_content.encode("utf-8"),
                    proxies=proxies,
                    timeout=30,
                )
                if retry_response.status_code == 200:
                    print(f"ntfy第 {actual_batch_num}/{total_batches} 批次重试成功 [{report_type}]")
                    success_count += 1
                else:
                    print(
                        f"ntfy第 {actual_batch_num}/{total_batches} 批次重试失败，状态码：{retry_response.status_code}"
                    )
            elif response.status_code == 413:
                print(
                    f"ntfy第 {actual_batch_num}/{total_batches} 批次消息过大被拒绝 [{report_type}]，消息大小：{batch_size} 字节"
                )
            else:
                print(
                    f"ntfy第 {actual_batch_num}/{total_batches} 批次发送失败 [{report_type}]，状态码：{response.status_code}"
                )
                try:
                    print(f"错误详情：{response.text}")
                except:
                    pass

        except requests.exceptions.ConnectTimeout:
            print(f"ntfy第 {actual_batch_num}/{total_batches} 批次连接超时 [{report_type}]")
        except requests.exceptions.ReadTimeout:
            print(f"ntfy第 {actual_batch_num}/{total_batches} 批次读取超时 [{report_type}]")
        except requests.exceptions.ConnectionError as e:
            print(f"ntfy第 {actual_batch_num}/{total_batches} 批次连接错误 [{report_type}]：{e}")
        except Exception as e:
            print(f"ntfy第 {actual_batch_num}/{total_batches} 批次发送异常 [{report_type}]：{e}")

    # 判断整体发送是否成功
    if success_count == total_batches:
        print(f"ntfy所有 {total_batches} 批次发送完成 [{report_type}]")
        return True
    elif success_count > 0:
        print(f"ntfy部分发送成功：{success_count}/{total_batches} 批次 [{report_type}]")
        return True  # 部分成功也视为成功
    else:
        print(f"ntfy发送完全失败 [{report_type}]")
        return False


def send_to_bark(
        bark_url: str,
        report_data: Dict,
        languages: List[str],
        report_type: str,
        update_info: Optional[Dict] = None,
        proxy_url: Optional[str] = None,
        mode: str = "daily",
        bark_batch_size: int = 3600,
        batch_send_interval: int = 3,
) -> bool:
    """发送到Bark（支持分批发送，使用纯文本格式）"""
    proxies = None
    if proxy_url:
        proxies = {"http": proxy_url, "https": proxy_url}

    # 获取分批内容（Bark 限制为 3600 字节以避免 413 错误）
    batches = split_content_into_batches(
        report_data, "wework", languages, update_info, max_bytes=bark_batch_size,
    )

    total_batches = len(batches)
    print(f"Bark消息分为 {total_batches} 批次发送 [{report_type}]")

    # 反转批次顺序，使得在Bark客户端显示时顺序正确
    # Bark显示最新消息在上面，所以我们从最后一批开始推送
    reversed_batches = list(reversed(batches))

    print(f"Bark将按反向顺序推送（最后批次先推送），确保客户端显示顺序正确")

    # 逐批发送（反向顺序）
    success_count = 0
    for idx, batch_content in enumerate(reversed_batches, 1):
        # 计算正确的批次编号（用户视角的编号）
        actual_batch_num = total_batches - idx + 1

        # 添加批次标识（使用正确的批次编号）
        if total_batches > 1:
            batch_header = f"[第 {actual_batch_num}/{total_batches} 批次]\n\n"
            batch_content = batch_header + batch_content

        # 清理 markdown 语法（Bark 不支持 markdown）
        plain_content = strip_markdown(batch_content)

        batch_size = len(plain_content.encode("utf-8"))
        print(
            f"发送Bark第 {actual_batch_num}/{total_batches} 批次（推送顺序: {idx}/{total_batches}），大小：{batch_size} 字节 [{report_type}]"
        )

        # 检查消息大小（Bark使用APNs，限制4KB）
        if batch_size > 4096:
            print(
                f"警告：Bark第 {actual_batch_num}/{total_batches} 批次消息过大（{batch_size} 字节），可能被拒绝"
            )

        # 构建JSON payload
        payload = {
            "title": report_type,
            "body": plain_content,
            "sound": "default",
            "group": "GithubHot",
        }

        try:
            response = requests.post(
                bark_url,
                json=payload,
                proxies=proxies,
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200:
                    print(f"Bark第 {actual_batch_num}/{total_batches} 批次发送成功 [{report_type}]")
                    success_count += 1
                    # 批次间间隔
                    if idx < total_batches:
                        time.sleep(batch_send_interval)
                else:
                    print(
                        f"Bark第 {actual_batch_num}/{total_batches} 批次发送失败 [{report_type}]，错误：{result.get('message', '未知错误')}"
                    )
            else:
                print(
                    f"Bark第 {actual_batch_num}/{total_batches} 批次发送失败 [{report_type}]，状态码：{response.status_code}"
                )
                try:
                    print(f"错误详情：{response.text}")
                except:
                    pass

        except requests.exceptions.ConnectTimeout:
            print(f"Bark第 {actual_batch_num}/{total_batches} 批次连接超时 [{report_type}]")
        except requests.exceptions.ReadTimeout:
            print(f"Bark第 {actual_batch_num}/{total_batches} 批次读取超时 [{report_type}]")
        except requests.exceptions.ConnectionError as e:
            print(f"Bark第 {actual_batch_num}/{total_batches} 批次连接错误 [{report_type}]：{e}")
        except Exception as e:
            print(f"Bark第 {actual_batch_num}/{total_batches} 批次发送异常 [{report_type}]：{e}")

    # 判断整体发送是否成功
    if success_count == total_batches:
        print(f"Bark所有 {total_batches} 批次发送完成 [{report_type}]")
        return True
    elif success_count > 0:
        print(f"Bark部分发送成功：{success_count}/{total_batches} 批次 [{report_type}]")
        return True  # 部分成功也视为成功
    else:
        print(f"Bark发送完全失败 [{report_type}]")
        return False
