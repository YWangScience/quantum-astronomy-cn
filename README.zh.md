# 量子天文学

[English README](README.md)

## 前言

写这本书的原因，是我想要学习量子天文学。

我最初想找一本从观测出发的教材，从真实的天文数据讲起，再逐步引入相干函数、光子统计、量子估计和仪器限制等等。我没有找到这样一本书。相关内容当然存在，许多论文和专著也写得很好，但它们分散在统计光学、量子光学、干涉测量、高能天体物理、宇宙学和量子信息里。

于是我决定自己写一本，也把写作当成学习的一部分。这本书仍然在更新，因为我仍然在学习。

<p align="right">王瑜<br>2026 年 7 月</p>

## 下载

- 在线英文书站：<https://book.quantum-astronomy.ywang.science>
- 中文 PDF：<https://github.com/YWangScience/quantum-astronomy/releases/latest/download/quantum-astronomy-cn.pdf>
- 英文 PDF：<https://github.com/YWangScience/quantum-astronomy/releases/latest/download/quantum-astronomy-en.pdf>
- Releases 页面：<https://github.com/YWangScience/quantum-astronomy/releases/latest>

## 本地编译

中文书稿从 `main.tex` 编译，生成文件写入 `build/`：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

生成的 PDF 位于 `build/main.pdf`。

当前中文排版使用 `qa-modern-clear.sty`，右侧留出公式解读区。新生成的编译文件请保留在
`build/`，不要放到仓库根目录。

## 目录

- 前言

### 快速入门

- 第一篇：什么是强度干涉

### 第一部分 基础、定义和观测量

- 第一章 最基础的概念
- 第二章 为什么需要量子天文学
- 第三章 量子光学基础
- 第四章 光子统计与相干函数

### 第二部分 仪器、强度干涉和信息极限

- 第五章 空间相干与强度干涉
- 第六章 探测器、时钟和事件表
- 第七章 事件表的数据分析
- 第八章 量子估计、Rayleigh 限制和亚分辨信息

### 第三部分 天体光源的量子语言

- 第九章 天体辐射机制的量子语言
- 第十章 恒星作为量子光源
- 第十一章 白矮星、中子星和强场物理
- 第十二章 黑洞、吸积盘和 photon ring
- 第十三章 爆发、瞬变和多信使量子天文学

### 第四部分 传播、宇宙学、新物理和量子网络

- 第十四章 传播效应：等离子体、尘埃和引力透镜
- 第十五章 暗物质、轴子和偏振量子通道
- 第十六章 宇宙学中的量子问题
- 第十七章 量子网络望远镜

### 第五部分 观测设计、案例、教学和路线图

- 第十八章 观测设计、误差预算和可行性计算
- 第十九章 第一代量子天文学科学案例
- 第二十章 教学实验和计算实验
- 第二十一章 常见误区
- 第二十二章 从白皮书到研究计划

### 附录

- 附录 A 常用公式索引
- 附录 B 常用单位和数值
- 附录 C 术语表
- 附录 D 核心关系的阅读路线和适用边界
- 附录 E 示例计算代码指南
- 附录 F 14 周课程安排建议
- 附录 G 文献导读
