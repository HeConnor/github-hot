#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/11/12
# @USER    : Shengji He
# @File    : st_ui.py
# @Software: PyCharm
# @Version  : Python-
# @TASK: example
import yaml
import streamlit as st
from datetime import datetime


def main():
    file = 'config.yaml'
    with open(file, 'r') as f:
        config = yaml.safe_load(f) or {}
    if 'languages' in config:
        languages = config['languages']
    else:
        languages = ["python", "javascript", "java", "c++", "c#", "go", "rust", "typescript"]
    file = r'./markdowns/2025-10-23.md'
    # 读取 Markdown 文件
    with open(file, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    # 页面配置
    st.set_page_config(
        page_title="Daily Github-Trending",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 创建上下布局
    upper_container = st.container()
    lower_container = st.container()
    # 上部：控件区域
    with upper_container:
        # 获取按钮
        get_button = st.button(
            "📥 获取",
            type="primary",
            use_container_width=True
        )
        # # st.header("🔧 控制面板")
        # # 创建两列布局，让界面更紧凑
        # col1, col2 = st.columns([3, 1])
        #
        # with col1:
        #     # st.subheader("编程语言")
        #     # 使用session_state保存复选框状态
        #     selected_languages = []
        #     for lang in languages:
        #         if st.checkbox(lang, key=f"lang_{lang}"):
        #             selected_languages.append(lang)
        #
        # with col2:
        #     # st.subheader("操作")
        #     # 获取按钮
        #     get_button = st.button(
        #         "📥 获取",
        #         type="primary",
        #         use_container_width=True
        #     )
    # 添加分隔符
    st.divider()

    # 下部：文档显示区域
    with lower_container:
        # 渲染到应用
        st.markdown(markdown_content)

    # 侧边栏：配置和信息
    with st.sidebar:
        st.header("⚙️ 配置")

        # 显示当前加载的编程语言
        # st.subheader("可选用的编程语言")
        # for lang in languages:
        #     st.write(f"- {lang}")
        selected_languages = []
        for lang in languages:
            if st.checkbox(lang, key=f"lang_{lang}"):
                selected_languages.append(lang)

        # st.subheader("关于")
        # st.info("""
        # 这个应用可以让你：
        # - 选择感兴趣的编程语言
        # - 获取相关的技术文档
        # - 以Markdown格式查看内容
        # """)


def main2():
    file = 'config.yaml'
    with open(file, 'r') as f:
        config = yaml.safe_load(f) or {}
    if 'languages' in config:
        languages = config['languages']
    else:
        languages = ["python", "javascript", "java", "c++", "c#", "go", "rust", "typescript"]
    file = r'./markdowns/2025-10-23.md'
    # 读取 Markdown 文件
    with open(file, "r", encoding="utf-8") as file:
        markdown_content = file.read()

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
        for lang in languages:
            if st.checkbox(lang, key=f"lang_{lang}"):
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
            # 示例逻辑：使用第一个选择的语言来决定文件，或者使用默认文件

            if not selected_langs:
                return "# 请选择至少一种编程语言\n\n请在侧边栏选择您感兴趣的编程语言，然后点击获取按钮。"

            # 假设我们有一个基础文件，然后根据语言进行过滤或增强
            base_file = './markdowns/2025-10-23.md'

            # if os.path.exists(base_file):
            #     with open(base_file, "r", encoding="utf-8") as file:
            #         content = file.read()
            #
            #     # 可以在这里根据 selected_langs 对内容进行过滤或处理
            #     # 例如，只显示与选定语言相关的内容
            #     processed_content = process_content_by_languages(content, selected_langs)
            #
            #     return processed_content
            # else:
            #     return f"# 文件未找到\n\n无法找到数据文件: {base_file}\n\n选择的语言: {', '.join(selected_langs)}"
            return markdown_content
        except Exception as e:
            return f"# 获取数据时出错\n\n错误信息: {str(e)}"

    # 处理按钮点击
    if get_button:
        if selected_languages:
            with st.spinner('正在获取最新数据...'):
                # 获取 Markdown 内容
                new_content = fetch_markdown_content(selected_languages)

                # 更新 session state
                st.session_state.markdown_content = new_content
                st.session_state.selected_languages = selected_languages.copy()
                st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 显示成功消息
                st.success(f"成功获取 {len(selected_languages)} 种语言的数据!")

                # 重新运行以立即显示新内容
                st.rerun()
        else:
            st.session_state.markdown_content = ""
            st.error("请先在侧边栏选择至少一种编程语言!")
    # 下部：文档显示区域
    with lower_container:
        # 渲染到应用
        # st.markdown(markdown_content)
        # 显示 Markdown 内容
        if st.session_state.markdown_content:
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


if __name__ == '__main__':
    main2()
    print('done')
