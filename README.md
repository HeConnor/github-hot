# github-hot

> copy from: [github-hot](https://github.com/shibing624/github-hot)

Tracking the hot Github repos and update daily

1. Automatically grab popular projects every day based on Github Actions [.github/workflows/schedule.yml](.github/workflows/schedule.yml)
2. Support project list output in markdown format, automatically synchronized to github
3. Support custom sorting, select topk hot interest repos

## Usage
```bash
git clone github-hot.git
cd github-hot
pip install -r requirements.txt
python crawler.py
```

### Result

<img src="./docs/pic.png" width="860" />


## License

授权协议为 [The Apache License 2.0](LICENSE)，可免费用做商业用途。请在产品说明中附加**github-hot**的链接和授权协议。


## Contribute
项目代码还很粗糙，如果大家对代码有所改进，欢迎提交回本项目，在提交之前，注意以下两点：

 - 在`tests`添加相应的单元测试
 - 使用`python -m pytest`来运行所有单元测试，确保所有单测都是通过的

之后即可提交PR。


## Related Projects

- javascript：[vitalets/github-trending-repos](https://github.com/vitalets/github-trending-repos)
