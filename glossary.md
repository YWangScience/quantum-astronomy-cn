# Glossary

This file is the working terminology index for the book. The polished reader-facing Chinese glossary is Appendix C in `appendices/zh/appendix_C.tex`. The bilingual translation glossary is `shared/terminology_zh_en.yml`. Use these files when editing chapters so the same concept is not renamed or redefined later.

## Editing Rules

- Define a term once at its first stable home, then refer back to that chapter or equation.
- Prefer the Chinese term listed here; keep the English form when it is a standard acronym or search keyword.
- Do not use "quantum" as a loose synonym for "single-photon", "low count", "precise", or "new physics".
- When adding a new term, record the first stable home, common confusions, and related terms.

## Core Data And Statistics

| Term | Preferred Chinese | English/Search Form | First Stable Home | Do Not Confuse With |
|---|---|---|---|---|
| 光子事件表 | 光子事件表 | photon event table | Chapter 1, Chapter 6 | 光变曲线、分箱计数 |
| 光变曲线 | 光变曲线 | light curve | Chapter 2 | 原始事件表 |
| 曝光函数 | 曝光函数 | exposure function | Chapter 7 | 墙钟积分时间 |
| 有效积分时间 | 有效积分时间 | live time | Chapter 6 | 总观测时长 |
| Poisson 过程 | Poisson 过程 | Poisson process | Chapter 1 | 任意低光子数数据 |
| 非齐次 Poisson 过程 | 非齐次 Poisson 过程 | inhomogeneous Poisson process | Chapter 7 | 稳态 Poisson |
| Cox process | Cox process | Cox process | Chapter 21 | 新物理非 Poisson |
| 似然 | 似然 | likelihood | Chapter 7 | 后验、概率密度的口语用法 |
| 后验 | 后验 | posterior | Chapter 7 | 似然 |
| Fisher 信息 | Fisher 信息 | Fisher information | Chapter 1, Chapter 7 | 直接观测精度 |
| 协方差矩阵 | 协方差矩阵 | covariance matrix | Chapter 7 | 独立误差条 |
| Fano factor | Fano factor | Fano factor | Chapter 21 | Mandel Q 参数 |
| trial factor | trial factor | trials factor | Chapter 21 | 单次 p-value |
| null test | null test | null test | Chapter 7, Chapter 21 | 普通画图检查 |

## Quantum Optics

| Term | Preferred Chinese | English/Search Form | First Stable Home | Do Not Confuse With |
|---|---|---|---|---|
| 模式 | 模式 | mode | Chapter 3 | 探测器通道 |
| 占有数 | 占有数 | occupation number | Chapter 3, Chapter 9 | 总光子数 |
| 相干态 | 相干态 | coherent state | Chapter 3 | 天体 maser 的全部情形 |
| 热态 | 热态 | thermal state | Chapter 3 | 任意黑体谱 |
| 压缩态 | 压缩态 | squeezed state | Chapter 3, Chapter 16 | 普通低噪声数据 |
| 密度矩阵 | 密度矩阵 | density matrix | Chapter 3 | 协方差矩阵 |
| 退相干 | 退相干 | decoherence | Chapter 3, Chapter 16 | 仪器噪声的笼统说法 |
| 一阶相干函数 | 一阶相干函数 | first-order coherence | Chapter 4 | 二阶强度相关 |
| 二阶相干函数 | 二阶相干函数 | second-order coherence, g2 | Chapter 4 | Poisson 计数率 |
| 聚束 | 聚束 | bunching | Chapter 1, Chapter 4 | 背景涨落 |
| 反聚束 | 反聚束 | antibunching | Chapter 4, Chapter 21 | \(g^{(2)}\simeq1\) |
| 相干时间 | 相干时间 | coherence time | Chapter 1, Chapter 4 | 采样时间 |
| Siegert 关系 | Siegert 关系 | Siegert relation | Chapter 1, Chapter 4 | 任意光场的恒等式 |
| Glauber 相关 | Glauber 相关 | Glauber correlation | Chapter 3, Chapter 4 | 经验相关系数 |

## Interferometry And Imaging

| Term | Preferred Chinese | English/Search Form | First Stable Home | Do Not Confuse With |
|---|---|---|---|---|
| 复可见度 | 复可见度 | complex visibility | Chapter 1, Chapter 5 | \(|V|^2\) |
| 基线 | 基线 | baseline | Chapter 5 | 投影基线 |
| 投影基线 | 投影基线 | projected baseline | Chapter 5 | 阵列物理距离 |
| \(u,v\) 覆盖 | \(u,v\) 覆盖 | uv coverage | Chapter 5, Chapter 18 | 单条基线长度 |
| VCZ 定理 | van Cittert--Zernike 定理 | VCZ theorem | Chapter 5 | Fourier optics 的全部内容 |
| 均匀圆盘 | 均匀圆盘 | uniform disk | Chapter 1, Chapter 5 | 边缘昏暗圆盘 |
| 边缘昏暗 | 边缘昏暗 | limb darkening | Chapter 10 | 仪器 vignetting |
| 强度干涉 | 强度干涉 | stellar intensity interferometry, SII | Chapter 5 | 振幅干涉 |
| 零基线对比度 | 零基线对比度 | zero-baseline contrast | Chapter 5, Chapter 18 | 零基线可见度 |
| 相位缺失 | 相位缺失 | phase loss | Chapter 5, Chapter 21 | 没有结构信息 |
| phase retrieval | 相位恢复 | phase retrieval | Chapter 5, Chapter 21 | 直接成像 |
| SPADE | SPADE/空间模式排序 | spatial-mode demultiplexing | Chapter 8 | 普通 PSF fitting |
| Rayleigh curse | Rayleigh curse | Rayleigh curse | Chapter 8 | 衍射极限本身 |
| 量子 Fisher 信息 | 量子 Fisher 信息 | quantum Fisher information | Chapter 8 | 经典 Fisher 信息 |

## Instruments And Calibration

| Term | Preferred Chinese | English/Search Form | First Stable Home | Do Not Confuse With |
|---|---|---|---|---|
| SPAD | SPAD | single-photon avalanche diode | Chapter 6 | 任意单光子探测器 |
| PMT | 光电倍增管 | photomultiplier tube | Chapter 6 | SPAD |
| TDC | TDC | time-to-digital converter | Chapter 6 | ADC |
| jitter | 时间抖动 | timing jitter | Chapter 6 | 采样 bin 宽 |
| 死时间 | 死时间 | dead time | Chapter 6 | 低效率 |
| afterpulsing | afterpulsing | afterpulsing | Chapter 6 | 天体短延迟相关 |
| 暗计数 | 暗计数 | dark count | Chapter 6 | 夜天光背景 |
| 电子串扰 | 电子串扰 | electronic crosstalk | Chapter 6, Chapter 21 | 天体零延迟峰 |
| White Rabbit | White Rabbit | White Rabbit timing | Chapter 6 | 普通网络时间 |
| 光谱通道 | 光谱通道 | spectral channel | Chapter 6, Chapter 22 | 单一滤光片 |
| 偏振通道 | 偏振通道 | polarization channel | Chapter 6, Chapter 15 | Stokes 参数本身 |
| 校准星 | 校准星 | calibrator star | Chapter 18 | 科学目标 |
| 系统误差地板 | 系统误差地板 | systematic floor | Chapter 18, Chapter 21 | 统计误差 |

## Sources, Propagation, And Cosmology

| Term | Preferred Chinese | English/Search Form | First Stable Home | Do Not Confuse With |
|---|---|---|---|---|
| 亮温 | 亮温 | brightness temperature | Chapter 9 | 真实热力学温度 |
| 热辐射 | 热辐射 | thermal emission | Chapter 9 | 热光统计的所有细节 |
| 同步辐射 | 同步辐射 | synchrotron radiation | Chapter 9 | 曲率辐射 |
| 逆康普顿散射 | 逆康普顿散射 | inverse Compton scattering | Chapter 9 | 同步自吸收 |
| maser | maser | astrophysical maser | Chapter 9, Chapter 21 | 稳定实验室 laser |
| 自然激光 | 自然激光 | natural laser | Chapter 19, Chapter 21 | \(g^{(2)}=1\) 的充分证据 |
| 宽线区 | 宽线区 | broad-line region, BLR | Chapter 12 | 吸积盘连续谱 |
| photon ring | photon ring | photon ring | Chapter 12 | EHT 图像全部结构 |
| Type Ia 超新星 | Type Ia 超新星 | Type Ia supernova | Chapter 13, Chapter 20 | 标准烛光的全部系统学 |
| DM | 色散量 | dispersion measure | Chapter 14 | 暗物质 DM |
| RM | 旋转量 | rotation measure | Chapter 14 | 仪器偏振角零点 |
| 散射展宽 | 散射展宽 | scattering broadening | Chapter 14 | 探测器 jitter |
| 时间延迟距离 | 时间延迟距离 | time-delay distance | Chapter 14 | 单个角直径距离 |
| 轴子双折射 | 轴子双折射 | axion birefringence | Chapter 15, Chapter 16 | 普通 Faraday 旋转 |
| CMB B 模 | CMB B 模 | CMB B-mode polarization | Chapter 16 | 所有偏振信号 |
| cosmic variance | cosmic variance | cosmic variance | Chapter 16 | 仪器误差 |

## Quantum Networks And Projects

| Term | Preferred Chinese | English/Search Form | First Stable Home | Do Not Confuse With |
|---|---|---|---|---|
| 量子网络望远镜 | 量子网络望远镜 | quantum-network telescope | Chapter 17 | 任何量子主题望远镜 |
| 纠缠分发率 | 纠缠分发率 | entanglement distribution rate | Chapter 17 | 天文光子率 |
| 量子存储 | 量子存储 | quantum memory | Chapter 17 | 普通数据缓存 |
| Bell fidelity | Bell 保真度 | Bell-state fidelity | Chapter 17 | 探测器效率 |
| 频率转换 | 频率转换 | quantum frequency conversion | Chapter 17 | 普通滤光片 |
| readiness | readiness | readiness | Chapter 22 | 口头“差不多可行” |
| milestone | 里程碑 | milestone | Chapter 22 | 章节小结 |
| data product | 数据产品 | data product | Chapter 22 | 论文图 |
| risk register | 风险登记表 | risk register | Chapter 22 | 普通待办清单 |
| 失败判据 | 失败判据 | failure criterion | Chapter 18, Chapter 22 | 负面结果本身 |
