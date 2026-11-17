# Publications 维护说明

网页默认按年份倒序展示，可切换为按研究领域分组，并可检索和筛选文献类型。不依赖GitHub Pages额外插件或浏览器端文献服务。

## 最新记录与CV存档

网页顶部链接到王炎教授持续维护的公开文献库：[ADS/SciX public library](https://scixplorer.org/public-libraries/sQDS-TmXS6qaQMMfZg6h5A)。它是查看最新记录的入口；站内列表是独立的静态副本，不会自动同步。链接名称与地址保存在`_data/publication_source.yml`。

- `local/publications/cv-publications.md`：完整CV论文清单，保留作者、题名、刊物、年份、类型、研究分类、DOI、arXiv和ADS链接，按年份倒序排列。
- `local/publications/archive/publications-2026-11-17.bib`：本次59条文献的原始导出快照，独立保留，不随当前列表更新而覆盖。
- `_data/publications.yml`和`files/publications.bib`：网站当前使用的数据及可下载BibTeX，继续作为日常维护文件。

更新网站数据后，可用下面的命令重新生成CV清单；需要保存当天的原始导出快照时追加`--archive-bibtex`。同一日期已有不同内容的快照时，工具会停止，避免覆盖旧档。

```sh
local/publications/.venv/bin/python local/publications/export_cv.py
```

如只更新了ADS/SciX而尚未重新导入，网页顶部的外部链接仍指向最新文献库；网页中的条目和CV清单则保留上次导入的内容。后续从该文献库导出完整BibTeX，再按下文批量更新即可。

## 直接维护

- `_data/publications.yml`：每篇文献的题名、作者、年份、月份、类型、研究类别、期刊及链接。
- `_data/publication_topics.yml`：网页中的研究类别及排列顺序。
- `_data/publication_source.yml`：最新文献库的显示名称及地址。
- `files/publications.bib`：供访问者下载的完整BibTeX。
- `_pages/publications.html`、`_includes/publication-entry.html`：页面和条目模板，通常不需要修改。
- `assets/css/publications.css`、`assets/js/publications.js`：页面专用样式和分组检索功能。

修改YAML后commit并push，GitHub Pages会按现有流程生成页面。作者名按导出记录保留，只有明确为Yan Wang的完整姓名才加粗，不根据模糊的Y. Wang推断身份。

每条文献的`sort_key`格式为`YYYY-MM-BibTeXKey`。年份相同则按月份从新到旧排序，月份相同按键名确定稳定顺序，不假设具体发表日。缺少月份时用`00`，不虚构月份。

`type`为`journal`、`preprint`或`conference`；`type_label`分别为Journal article、Preprint、Conference paper。arXiv记录不等于已获期刊接收；正式发表后，应以期刊元数据更新同一条记录，而不是重复添加预印本和期刊版本。

`topic`须与`_data/publication_topics.yml`中的类别ID一致，`topic_label`是该类别的显示名称。研究类别是按标题和关键词人工拟定的主类别，跨领域论文可按实际重点调整。

## 从BibTeX批量更新

首次使用时在本机准备独立环境：

```sh
python3 -m venv local/publications/.venv
local/publications/.venv/bin/pip install -r local/publications/requirements.txt
```

将完整ADS导出文件放到`files/publications.bib`，在`local/publications/topics.yml`的`assignments`中为新增的BibTeX键指定类别，然后运行：

```sh
local/publications/.venv/bin/python local/publications/import_bibtex.py files/publications.bib
```

也可以把其他位置的BibTeX文件作为参数，脚本会同时更新下载文件。导入器检查重复键、重复DOI、可能重复的题名和缺失分类；成功后生成网页数据。原始ADS导出不包含完整作者列表的记录保留et al.，不会补造作者。

注意：批量导入会重新生成YAML。已直接修改YAML的元数据应先同步回BibTeX；分类调整同时同步到topics.yml。不要把只含新增论文的文件当作完整清单重新导入。

本目录`local/`已被现有Jekyll配置排除，不会出现在公开网站中。这里的工具不参与GitHub Pages构建，不需要在GitHub安装Python依赖。
