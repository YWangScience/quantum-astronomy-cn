# Continuity Log

## 2026-07-01 Consistency Pass

Global rule added during the consistency pass: a concept, estimator, or core formula should be defined at its first stable home, then reused by `\ref` or `\eqref` in later chapters. Later chapters should explain the new physical situation, parameter values, observational use, and failure modes, not repeat the original definition.

Current stable homes:
- Event row and first-pass observables: Chapter 1, with raw instrument fields expanded in Chapter 6.
- Poisson likelihood, correlation estimators, covariance, and Fisher workflow: Chapters 1 and 7.
- Visibility, uniform disk, Siegert relation, VCZ theorem, SII SNR, baseline counting, and phase ambiguity: Chapters 1 and 5.
- SPADE, Rayleigh-limit Fisher information, and Cramér--Rao language: Chapter 8.
- Quantum-network rate, memory, and fidelity constraints: Chapter 17.
- Observing error budget and feasibility language: Chapter 18.
- Teaching experiments and proposal checklists: Chapters 20--22.

Appendices now act as index, unit quick reference, glossary, reading route, code guide, course schedule, and literature guide. They should not rederive or restate equations already introduced in the chapters unless a later explicit appendix project requires a full derivation.

## Chapter 1: 数学和物理基础
Book role: 数学和物理基础；起点：本章目的。
Concepts introduced: 本章目的, 复数、相位和干涉, 傅里叶变换和天空亮度, 概率分布、矩和阶乘矩
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 2: 为什么需要量子天文学
Book role: 为什么需要量子天文学；起点：天文学通常测量什么。
Concepts introduced: 天文学通常测量什么, 平均强度会丢掉什么, 一个简单例子：热光和激光可以一样亮, 从 Sirius 到现代强度干涉
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 3: 量子光学基础
Book role: 量子光学基础；起点：电磁场模式和光子。
Concepts introduced: 电磁场模式和光子, 常见光态, 光场的相空间表示, 密度矩阵和退相干
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 4: 光子统计与相干函数
Book role: 光子统计与相干函数；起点：从光子计数开始。
Concepts introduced: 从光子计数开始, 一阶相干函数, 二阶相干函数, Siegert 关系
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 5: 空间相干与强度干涉
Book role: 空间相干与强度干涉；起点：一阶空间相干。
Concepts introduced: 一阶空间相干, van Cittert-Zernike 定理, HBT 空间强度干涉, 强度干涉信噪比
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 6: 探测器、时钟和事件表
Book role: 探测器、时钟和事件表；起点：为什么事件表是核心数据。
Concepts introduced: 为什么事件表是核心数据, 单光子探测器类型, 探测器性能参数, 时间同步
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 7: 事件表的数据分析
Book role: 事件表的数据分析；起点：从事件表到相关函数。
Concepts introduced: 从事件表到相关函数, 时间校正, 随机符合和背景估计, 相关算法
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 8: 量子估计、Rayleigh 限制和亚分辨信息
Book role: 量子估计、Rayleigh 限制和亚分辨信息；起点：Rayleigh 判据不是最终答案。
Concepts introduced: Rayleigh 判据不是最终答案, Fisher 信息和量子 Fisher 信息, 双点源超分辨, 强度干涉中的量子估计
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 9: 天体辐射机制的量子语言
Book role: 天体辐射机制的量子语言；起点：为什么重新看辐射机制。
Concepts introduced: 为什么重新看辐射机制, 热辐射, 自由自由和自由束缚辐射, 同步辐射
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 10: 恒星作为量子光源
Book role: 恒星作为量子光源；起点：恒星光为什么近似热光。
Concepts introduced: 恒星光为什么近似热光, 角直径和有效温度, 表面结构, 双星和多星
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 11: 白矮星、中子星和强场物理
Book role: 白矮星、中子星和强场物理；起点：白矮星：最大的量子天体之一。
Concepts introduced: 白矮星：最大的量子天体之一, 吸积白矮星和磁场, 中子星和脉冲星, 磁星和强场 QED
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 12: 黑洞、吸积盘和 photon ring
Book role: 黑洞、吸积盘和 photon ring；起点：黑洞附近的光学发射。
Concepts introduced: 黑洞附近的光学发射, 活动星系核宽线区, 喷流和 blazar, photon ring 和强引力时间结构
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 13: 爆发、瞬变和多信使量子天文学
Book role: 爆发、瞬变和多信使量子天文学；起点：为什么瞬变重要。
Concepts introduced: 为什么瞬变重要, 新星, Type Ia 超新星, 核心坍缩超新星
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 14: 传播效应：等离子体、尘埃和引力透镜
Book role: 传播效应：等离子体、尘埃和引力透镜；起点：传播可以看成量子通道。
Concepts introduced: 传播可以看成量子通道, 等离子体色散, 散射和闪烁, 尘埃吸收、散射和偏振
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 15: 暗物质、轴子和偏振量子通道
Book role: 暗物质、轴子和偏振量子通道；起点：轻场和偏振旋转。
Concepts introduced: 轻场和偏振旋转, 为什么量子天文学有新信息, 脉冲星偏振阵列, 快速射电暴和重复源
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 16: 宇宙学中的量子问题
Book role: 宇宙学中的量子问题；起点：CMB 是什么样的光场。
Concepts introduced: CMB 是什么样的光场, 暴胀涨落作为压缩态, 量子到经典的转变, CMB 偏振和宇宙双折射
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 17: 量子网络望远镜
Book role: 量子网络望远镜；起点：传统振幅干涉的限制。
Concepts introduced: 传统振幅干涉的限制, quantum telescopy 的基本思想, 量子中继和纠缠分发, 连续变量 teleportation 方案
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 18: 观测设计、误差预算和可行性计算
Book role: 观测设计、误差预算和可行性计算；起点：从科学问题到观测量。
Concepts introduced: 从科学问题到观测量, 光子率估算, 相关信号的数量级, 基线选择
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 19: 第一代量子天文学科学案例
Book role: 第一代量子天文学科学案例；起点：案例选择原则。
Concepts introduced: 案例排序, 恒星角直径和有效温度, 快速自转, 双星、Be/WR 谱线区和瞬变, Crab 统计和自然激光
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 20: 教学实验和计算实验
Book role: 教学实验和计算实验；起点：实验一：LED、激光和热光的 \(g^{(2)}\)。
Concepts introduced: 事件表和桌面 HBT, 均匀圆盘和双星, 事件表相关器, Rayleigh curse 和 SPADE, Type Ia 距离 toy model
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 21: 常见误区
Book role: 常见误区；起点：看到光子不等于量子天文学。
Concepts introduced: 看到光子不等于量子天文学, \(g^{(2)}=1\) 的边界, 强度干涉校准, 相位缺失和成像, 超分辨适用条件, 假警报和新物理边界
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.

## Chapter 22: 从白皮书到研究计划
Book role: 从白皮书到研究计划；起点：2026 到 2030：强度干涉的工程化。
Concepts introduced: 2026 到 2030：强度干涉数据产品, 2030 到 2040：多通道事件表, 2040 以后：量子网络望远镜, 研究计划和风险登记
Terms defined: see glossary.md and the local section definitions.
Symbols introduced: see notation.md and equations in the chapter.
Equations introduced: see chapter text.
Claims established: Key claims are maintained in the chapter text and cross-references.
Assumptions made: textbook-level approximations are stated locally with ADS citations where needed.
Limitations stated: each section includes system-error or scope language.
Open questions left for later chapters: deeper implementation details and science cases are deferred according to the outline.
Dependencies created for later chapters: terminology, notation, and observables used by subsequent chapters.
Possible conflicts with previous chapters: checked during rolling consistency passes; recheck after major rewrites.
