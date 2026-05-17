#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/11/13
# @File    : app.py
# @Software: PyCharm
# @Version  : Python-
# @TASK:
import streamlit as st
from datetime import datetime
from crawler import scrape
from utils import load_config


def main():
    LANGUAGES = ["python", 'jupyter-notebook', "javascript", "java", "c++", "c#", "go", "rust", "typescript"]

    file = 'config.yaml'
    config = load_config(file)
    languages_cfg = []
    if 'languages' in config:
        languages_cfg = config['languages']

    default_content = None

    # 初始化 session state
    if 'markdown_content' not in st.session_state:
        st.session_state.markdown_content = ""
    if 'last_updated' not in st.session_state:
        st.session_state.last_updated = None
    if 'selected_languages' not in st.session_state:
        st.session_state.selected_languages = []

    # 页面配置
    st.set_page_config(
        page_title="Daily Github-Trending",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 创建上下布局
    upper_container = st.container()
    lower_container = st.container()

    # 侧边栏：配置和信息
    with st.sidebar:
        st.header("⚙️ 配置")

        selected_languages = []
        for lang in LANGUAGES:
            val = True if lang in languages_cfg else False
            if st.checkbox(lang, val, key=f"lang_{lang}"):
                selected_languages.append(lang)

        # 显示上次更新时间
        if st.session_state.last_updated:
            st.caption(f"最后更新: {st.session_state.last_updated}")

    # 上部：控件区域
    with upper_container:
        # # 获取按钮
        # get_button = st.button(
        #     "📥 获取",
        #     type="primary",
        #     use_container_width=True
        # )
        col1, col2 = st.columns([1, 4])
        with col1:
            # 获取按钮
            get_button = st.button(
                "📥 获取",
                type="primary",
                use_container_width=True,
                # 添加 tooltip
                help="根据选择的编程语言获取最新的 Github Trending 数据"
            )

        with col2:
            # 显示状态信息
            if st.session_state.last_updated:
                st.success(f"数据已更新 ({st.session_state.last_updated})")
            else:
                st.info("点击获取按钮加载数据")

    # 添加分隔符
    st.divider()

    # 获取数据的函数
    def fetch_markdown_content(selected_langs):
        """根据选择的编程语言获取对应的 Markdown 内容"""
        try:
            # 这里可以根据选择的语言来获取不同的 Markdown 文件
            if not selected_langs:
                return "# 请选择至少一种编程语言\n\n请在侧边栏选择您感兴趣的编程语言，然后点击获取按钮。"

            processed_content = ''
            for selected_lang in selected_langs:
                # print(selected_lang)
                try:
                    processed_content += scrape(selected_lang, None, 10)
                except Exception as e:
                    processed_content += f'\n### {selected_lang}\n {e}\n'
            return processed_content
        except Exception as e:
            return f"# 获取数据时出错\n\n错误信息: {str(e)}"

    # 处理按钮点击
    if get_button:
        if default_content is None:
            default_content = scrape('', None, 10)
            # default_content = ""
        if selected_languages:
            with st.spinner('正在获取最新数据...'):
                # 获取 Markdown 内容
                new_content = fetch_markdown_content(selected_languages)

                # 更新 session state
                st.session_state.markdown_content = default_content + new_content
                st.session_state.selected_languages = selected_languages.copy()
                st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 显示成功消息
                st.success(f"成功获取 {len(selected_languages)} 种语言的数据!")

                # 重新运行以立即显示新内容
                st.rerun()
        else:
            st.session_state.markdown_content = default_content
            st.error("请先在侧边栏选择至少一种编程语言!")
    # 下部：文档显示区域
    with lower_container:
        if st.session_state.selected_languages:
            st.markdown(st.session_state.markdown_content)
        else:
            # 初始状态显示提示
            st.info("""
                    ## 欢迎使用 Daily Github-Trending

                    使用步骤:
                    1. 查看最新的 Github Trending 项目
                    2. 在左侧边栏选择您感兴趣的编程语言
                    3. 点击上方的"获取"按钮

                    📊 数据将根据您选择的语言进行筛选和显示
                    """)
            st.markdown(st.session_state.markdown_content)


if __name__ == '__main__':
    main()
    print('done')
