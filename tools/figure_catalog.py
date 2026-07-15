#!/usr/bin/env python3
"""Figure catalog for the quantum astronomy textbook.

Each entry describes one generated figure. The plotting-code generator uses the
same file names, and the LaTeX generator uses the captions and section keywords
to place figures near the relevant text.
"""

from __future__ import annotations


FIGURES: list[dict[str, object]] = [
    {
        "chapter": 1,
        "filename": "ch01_fourier_visibility.pdf",
        "section_keywords": ["傅里叶", "天空亮度", "复数"],
        "caption": "高斯、双星和均匀圆盘三类亮度分布给出不同的归一化可见度曲线。源的角尺度越大，可见度在空间频率轴上下降越快；双星的振荡项保留了角分离信息。",
    },
    {
        "chapter": 1,
        "filename": "ch01_photon_count_statistics.pdf",
        "section_keywords": ["概率分布", "factorial", "Poisson"],
        "caption": "相同平均光子数下，Poisson 分布、单模热光分布和亚 Poisson toy model 的宽度不同。计数分布的方差决定 Mandel Q 参数，也决定二阶相干函数偏离 1 的方向。",
    },
    {
        "chapter": 1,
        "filename": "ch01_resolution_baseline.pdf",
        "section_keywords": ["数量级", "分辨率", "基线"],
        "caption": "角分辨率随波长和基线的标度。可见光进入微角秒量级需要百米到公里级基线；同一公式也说明为什么长基线和短波长是高角分辨率观测的核心资源。",
    },
    {
        "chapter": 1,
        "filename": "ch01_correlation_dilution_budget.pdf",
        "section_keywords": ["HBT", "稀释", "背景"],
        "caption": "HBT 相关峰的可见幅度同时受光谱带宽、时间分辨率和背景稀释控制；源光子比例下降时相关幅度按两通道比例乘积损失。",
    },
    {
        "chapter": 1,
        "filename": "ch01_polarization_mueller_matrix.pdf",
        "section_keywords": ["Mueller", "偏振", "矩阵"],
        "caption": "Mueller 矩阵中的小串扰会把真实 Stokes 向量推到错误位置，弱偏振信号尤其容易被 I 到 Q/U 泄漏污染。",
    },
    {
        "chapter": 1,
        "filename": "ch01_fisher_visibility_design.pdf",
        "section_keywords": ["Fisher", "误差", "可见度"],
        "caption": "Fisher 信息由可见度曲线斜率、误差模型和有效光子对共同决定；统计误差下降到系统地板后，继续积分收益变小。",
    },
    {
        "chapter": 2,
        "filename": "ch02_mean_intensity_vs_correlation.pdf",
        "section_keywords": ["平均强度", "丢掉", "热光"],
        "caption": "两束光可以有相同的平均强度和光变曲线，却有不同的二阶相干函数。平均强度只记录一阶统计量，光子到达时间之间的联合概率保存在 g2 中。",
    },
    {
        "chapter": 2,
        "filename": "ch02_event_table_information.pdf",
        "section_keywords": ["光子事件表", "工作定义", "观测量"],
        "caption": "光子事件表把时间、望远镜位置、频率通道和偏振标签放在同一个数据结构中。不同的边缘化方式分别给出光变曲线、谱线、偏振量和强度相关函数。",
    },
    {
        "chapter": 2,
        "filename": "ch02_contrast_dilution.pdf",
        "section_keywords": ["热光", "多模", "时间分辨率"],
        "caption": "观测到的二阶相关对比度会被有效模式数、光谱带宽和时间 bin 同时稀释。",
    },
    {
        "chapter": 2,
        "filename": "ch02_revival_timeline.pdf",
        "section_keywords": ["HBT", "Narrabri", "复兴"],
        "caption": "从 HBT、Narrabri 到现代 Cherenkov 阵列的时间线，突出沉寂期的工程瓶颈和数字相关带来的复兴。",
    },
    {
        "chapter": 2,
        "filename": "ch02_science_case_map.pdf",
        "section_keywords": ["科学问题", "可行性", "路线图"],
        "caption": "第一代量子天文学科学问题的可行性和新增信息量，显示亮星角直径、Be 星盘、自然 laser、Type Ia 和量子网络的相对位置。",
    },
    {
        "chapter": 3,
        "filename": "ch03_phase_space_states.pdf",
        "section_keywords": ["相干态", "密度矩阵", "非经典"],
        "caption": "相干态、热态和压缩态在相空间中的示意。相干态近似圆形最小不确定度分布，热态更宽，压缩态在一个正交量上变窄但在另一个正交量上变宽。",
    },
    {
        "chapter": 3,
        "filename": "ch03_coherence_time_dilution.pdf",
        "section_keywords": ["相干时间", "有限时间", "光谱带宽"],
        "caption": "有限时间分辨率会稀释热光聚束信号。当时间 bin 大于相干时间时，测得的 g2 峰值按相干时间与 bin 宽的比值下降；多模平均会进一步降低对比度。",
    },
    {
        "chapter": 3,
        "filename": "ch03_state_count_distributions.pdf",
        "section_keywords": ["数态", "热态", "计数分布"],
        "caption": "数态、相干态和热态在相同平均光子数附近给出不同计数分布，直接对应不同的 g2(0)。",
    },
    {
        "chapter": 3,
        "filename": "ch03_blackbody_mode_occupation.pdf",
        "section_keywords": ["亮温", "弱光", "占有数"],
        "caption": "不同亮温黑体的单模占有数随波长变化，显示可见光恒星通常处在每模式弱光极限。",
    },
    {
        "chapter": 3,
        "filename": "ch03_detection_loss_background.pdf",
        "section_keywords": ["损耗", "背景", "探测器"],
        "caption": "有限探测效率、天空背景和暗计数会降低源光子比例，并按比例平方稀释归一化相关幅度。",
    },
    {
        "chapter": 3,
        "filename": "ch03_nonclassical_mixing_boundary.pdf",
        "section_keywords": ["非经典", "反聚束", "背景"],
        "caption": "背景和多源混合会把反聚束或热光聚束信号拉回 g2=1，说明天体非经典光为什么难以保留。",
    },
    {
        "chapter": 4,
        "filename": "ch04_mandel_q_g2.pdf",
        "section_keywords": ["Mandel", "Poisson", "二阶"],
        "caption": "Mandel Q 参数把计数方差和 g2 的零延迟值联系起来。Q 大于零对应超 Poisson 统计，Q 等于零回到 Poisson 线，Q 小于零则表示亚 Poisson 统计。",
    },
    {
        "chapter": 4,
        "filename": "ch04_siegert_relation.pdf",
        "section_keywords": ["Siegert", "一阶", "二阶"],
        "caption": "Siegert 关系把热光的一阶相干函数和二阶强度相关联系起来。一阶相干随延迟衰减时，二阶相干峰以其模平方的形式变窄并回到 1。",
    },
    {
        "chapter": 4,
        "filename": "ch04_factorial_moments.pdf",
        "section_keywords": ["factorial", "事件表", "高阶"],
        "caption": "普通矩和 factorial moment 对同一计数分布给出不同权重。符合计数天然依赖 N 乘以 N-1，因此 factorial moment 比普通二阶矩更贴近多光子探测问题。",
    },
    {
        "chapter": 4,
        "filename": "ch04_response_convolution.pdf",
        "section_keywords": ["时间响应", "卷积", "相干时间"],
        "caption": "有限时间响应会把 ps 量级热光聚束峰拉宽并压低，峰高按响应宽度与相干时间的比值下降。",
    },
    {
        "chapter": 4,
        "filename": "ch04_delay_histogram_estimator.pdf",
        "section_keywords": ["延迟直方图", "估计量", "事件表"],
        "caption": "延迟直方图估计量通过同源符合和移位参考的差值恢复 g2-1 的小 excess。",
    },
    {
        "chapter": 4,
        "filename": "ch04_deadtime_pileup_bias.pdf",
        "section_keywords": ["死时间", "pile-up", "afterpulsing"],
        "caption": "死时间、pile-up 和 afterpulsing 会在短延迟相关中制造空洞和假峰，分束交叉相关可减轻这些仪器效应。",
    },
    {
        "chapter": 4,
        "filename": "ch04_g3_closure_phase.pdf",
        "section_keywords": ["三阶相关", "闭合相位", "相位恢复"],
        "caption": "三阶强度相关包含 gamma12 gamma23 gamma31 的实部，因此对闭合相位组合敏感。",
    },
    {
        "chapter": 4,
        "filename": "ch04_frequency_polarization_matrix.pdf",
        "section_keywords": ["频率", "偏振", "相关矩阵"],
        "caption": "频率和偏振分辨 g2 可以写成跨通道矩阵，谱线通道和同偏振通道通常有更高 excess。",
    },
    {
        "chapter": 5,
        "filename": "ch05_vcz_visibility_models.pdf",
        "section_keywords": ["van Cittert", "空间相干", "可见度"],
        "caption": "van Cittert-Zernike 定理把天空亮度分布和空间相干函数联系起来。圆盘、环和双源在可见度空间留下不同的零点、振荡和包络。",
    },
    {
        "chapter": 5,
        "filename": "ch05_sii_signal_vs_baseline.pdf",
        "section_keywords": ["强度干涉", "HBT", "基线"],
        "caption": "强度干涉测得的相关信号正比于可见度模平方。较大的角直径在较短基线上就被分辨，因此 g2 相关信号随基线更快下降。",
    },
    {
        "chapter": 5,
        "filename": "ch05_uv_coverage.pdf",
        "section_keywords": ["地球自转", "u,v", "成像"],
        "caption": "地球自转把固定望远镜基线投影到不同的 u,v 位置。覆盖越稠密，重建二维亮度分布时对模型假设的依赖越低。",
    },
    {
        "chapter": 5,
        "filename": "ch05_uniform_disk_resolution.pdf",
        "section_keywords": ["均匀圆盘", "第一零点", "角直径"],
        "caption": "均匀圆盘第一零点基线随角直径变化，展示蓝光 SII 进入亚毫角秒和几十微角秒尺度所需的基线。",
    },
    {
        "chapter": 5,
        "filename": "ch05_snr_scaling.pdf",
        "section_keywords": ["SNR", "星等", "电子带宽"],
        "caption": "强度干涉 SNR 随星等、积分时间和电子带宽的相对标度，显示亮星选择和高速电子学为什么关键。",
    },
    {
        "chapter": 5,
        "filename": "ch05_zero_baseline_calibration.pdf",
        "section_keywords": ["零基线", "N0", "校准"],
        "caption": "零基线相关幅度 N0 的夜间漂移会整体拉伸 |V|2，直接影响角直径和形状拟合。",
    },
    {
        "chapter": 5,
        "filename": "ch05_phase_ambiguity.pdf",
        "section_keywords": ["相位", "退化", "成像"],
        "caption": "源和镜像源可以有相同的 |V|2，说明只测模平方会丢失 Fourier 相位并产生成像退化。",
    },
    {
        "chapter": 5,
        "filename": "ch05_error_budget.pdf",
        "section_keywords": ["误差预算", "系统误差", "强度干涉"],
        "caption": "强度干涉角直径误差由统计、零基线、背景、模型和选择函数共同组成，现代阵列不只受 photon noise 限制。",
    },
    {
        "chapter": 6,
        "filename": "ch06_detector_timing_response.pdf",
        "section_keywords": ["时间同步", "探测器", "时间"],
        "caption": "探测器时间响应会把真实相关峰卷积变宽并降低峰值。相关峰的面积近似守恒，但峰高决定了有限计数下能否显著检出。",
    },
    {
        "chapter": 6,
        "filename": "ch06_deadtime_saturation.pdf",
        "section_keywords": ["探测器性能", "事件表", "单光子"],
        "caption": "探测器死时间会使观测计数率在高入射光子率下饱和。非延长和延长死时间模型的偏差不同，必须在事件表分析前单独标定。",
    },
    {
        "chapter": 7,
        "filename": "ch07_poisson_likelihood.pdf",
        "section_keywords": ["事件表", "似然", "Poisson"],
        "caption": "非齐次 Poisson 过程把瞬时光子率映射为事件到达时间。似然函数同时使用每个事件位置处的率和整个观测窗口中的积分率。",
    },
    {
        "chapter": 7,
        "filename": "ch07_covariance_matrix.pdf",
        "section_keywords": ["协方差", "相关", "矩阵"],
        "caption": "多望远镜事件表可以写成协方差矩阵。对角项主要记录单通道噪声，非对角项记录望远镜对之间的真实相关和系统串扰。",
    },
    {
        "chapter": 7,
        "filename": "ch07_fisher_scaling.pdf",
        "section_keywords": ["Fisher", "误差", "模型拟合"],
        "caption": "参数误差随 Fisher 信息增加而下降。对于独立事件，信息量通常近似随有效光子数线性增加，因此误差按光子数的平方根标度下降。",
    },
    {
        "chapter": 8,
        "filename": "ch08_rayleigh_information.pdf",
        "section_keywords": ["Rayleigh", "Fisher", "亚分辨"],
        "caption": "Rayleigh 判据给出成像分辨的经验尺度，但参数估计的信息量不必在该尺度处突然消失。直接成像和模式测量在小分离极限下有不同的信息行为。",
    },
    {
        "chapter": 8,
        "filename": "ch08_spade_probabilities.pdf",
        "section_keywords": ["SPADE", "双点源", "模式"],
        "caption": "SPADE 把两点源分离信息转移到高阶空间模式的占有概率中。小分离时零阶模式仍占主导，高阶模式的微小概率携带了分离参数的信息。",
    },
    {
        "chapter": 8,
        "filename": "ch08_cramer_rao_bound.pdf",
        "section_keywords": ["Cram", "参数", "先验"],
        "caption": "Cramer-Rao 下界给出无偏估计量方差的理想下限。随着光子数增加，统计下限下降；加入背景或模型不匹配后，误差会出现平台。",
    },
    {
        "chapter": 9,
        "filename": "ch09_radiation_g2_diagnostics.pdf",
        "section_keywords": ["热辐射", "同步辐射", "谱线"],
        "caption": "不同辐射机制可以有相同的平均亮度，却在 g2 延迟曲线上表现不同。热辐射产生聚束峰，相干或受激成分会把曲线推向 Poisson 极限。",
    },
    {
        "chapter": 9,
        "filename": "ch09_diagnostic_plane.pdf",
        "section_keywords": ["统一诊断", "散射", "随机激光"],
        "caption": "谱宽、偏振度和二阶相干对比度共同组成辐射机制诊断平面。单一观测量通常不足以区分热辐射、同步辐射、maser 和散射放大。",
    },
    {
        "chapter": 10,
        "filename": "ch10_stellar_diameter_visibility.pdf",
        "section_keywords": ["角直径", "恒星", "有效温度"],
        "caption": "恒星角直径决定可见度模平方随基线下降的速度。强度干涉直接测量的是这个下降曲线，而不是图像中的恒星边缘。",
    },
    {
        "chapter": 10,
        "filename": "ch10_binary_visibility.pdf",
        "section_keywords": ["双星", "多星", "表面结构"],
        "caption": "双星会在可见度空间中产生周期性振荡。振荡周期主要由角分离决定，振幅则受流量比和单星角直径调制。",
    },
    {
        "chapter": 10,
        "filename": "ch10_limb_darkening.pdf",
        "section_keywords": ["边缘昏暗", "表面结构", "恒星"],
        "caption": "边缘昏暗改变圆盘亮度分布，也改变可见度零点和旁瓣高度。精密角直径和有效温度估计需要把这种表面亮度模型写进拟合。",
    },
    {
        "chapter": 11,
        "filename": "ch11_stokes_qu_track.pdf",
        "section_keywords": ["偏振", "Stokes", "Mueller"],
        "caption": "Q-U 平面中的轨迹显示偏振角旋转如何改变观测 Stokes 参数。强场源的偏振信号必须和仪器 Mueller 矩阵共同拟合。",
    },
    {
        "chapter": 11,
        "filename": "ch11_birefringence_energy.pdf",
        "section_keywords": ["强场", "QED", "磁星"],
        "caption": "强场双折射或传播效应可以让偏振角随能量发生系统旋转。观测上需要同时比较偏振角、偏振度和仪器响应随能量的变化。",
    },
    {
        "chapter": 12,
        "filename": "ch12_photon_ring_visibility.pdf",
        "section_keywords": ["photon ring", "黑洞", "可见度"],
        "caption": "薄环 toy model 的可见度模平方出现振荡零点。黑洞 photon ring 的几何尺度越清楚，长基线可见度中的振荡结构越容易成为可测量目标。",
    },
    {
        "chapter": 12,
        "filename": "ch12_variability_autocorrelation.pdf",
        "section_keywords": ["时间结构", "吸积盘", "光变"],
        "caption": "吸积流的短时标涨落会在自相关函数中留下特征宽度。事件表保留单光子时间信息后，可以把平均光变和相关时间尺度分开估计。",
    },
    {
        "chapter": 13,
        "filename": "ch13_transient_event_likelihood.pdf",
        "section_keywords": ["瞬变", "爆发", "似然"],
        "caption": "瞬变事件表的似然来自时间依赖光子率。快上升慢下降的率模型对应非均匀事件密度，触发时间和背景项都会影响参数后验。",
    },
    {
        "chapter": 13,
        "filename": "ch13_multimessenger_delay.pdf",
        "section_keywords": ["多信使", "引力波", "瞬变"],
        "caption": "多信使观测比较的是不同信号通道的到达时间和不确定度。真正的物理延迟必须和触发误差、传播效应以及仪器时间基准一起建模。",
    },
    {
        "chapter": 14,
        "filename": "ch14_dispersion_delay.pdf",
        "section_keywords": ["等离子体", "色散", "FRB"],
        "caption": "冷等离子体色散使低频光子相对高频光子更晚到达。延迟随频率平方倒数变化，因此宽频段事件表能同时约束 DM 和本征发射时间。",
    },
    {
        "chapter": 14,
        "filename": "ch14_faraday_rotation.pdf",
        "section_keywords": ["Faraday", "偏振", "等离子体"],
        "caption": "Faraday 旋转让偏振角随波长平方线性变化。斜率给出 RM，但偏振角的模 pi 周期性会在窄频段中引入缠绕歧义。",
    },
    {
        "chapter": 14,
        "filename": "ch14_lensing_time_delay.pdf",
        "section_keywords": ["引力透镜", "时间延迟", "尘埃"],
        "caption": "简化透镜势给出多像位置和时间延迟面。量子天文学中的透镜问题仍然要回到可观测的到达时间、放大率和角位置。",
    },
    {
        "chapter": 15,
        "filename": "ch15_axion_conversion.pdf",
        "section_keywords": ["轴子", "暗物质", "偏振"],
        "caption": "轴子-光子耦合的 toy model 展示转换概率如何随有效耦合、路径长度和相干长度变化。图只说明标度关系，不代表具体实验排除线。",
    },
    {
        "chapter": 15,
        "filename": "ch15_cosmic_birefringence.pdf",
        "section_keywords": ["宇宙双折射", "偏振", "新物理"],
        "caption": "宇宙双折射会把线偏振角整体旋转，并在 Q-U 平面中表现为同心轨迹。真正的宇宙学约束需要同时控制仪器偏振角标定。",
    },
    {
        "chapter": 15,
        "filename": "ch15_dark_matter_lensing.pdf",
        "section_keywords": ["暗物质", "透镜", "小尺度"],
        "caption": "小尺度质量结构会改变透镜放大率和到达时间。微小扰动不应直接解释为新物理，必须先和源结构、传播效应和仪器系统误差比较。",
    },
    {
        "chapter": 16,
        "filename": "ch16_cmb_power_spectrum.pdf",
        "section_keywords": ["CMB", "宇宙学", "量子涨落"],
        "caption": "CMB 角功率谱把早期涨落投影到多极矩空间。峰的位置和高度分别反映角尺度、物质组分和声学振荡历史；图为教学 toy model。",
    },
    {
        "chapter": 16,
        "filename": "ch16_birefringence_eb.pdf",
        "section_keywords": ["CMB 偏振", "宇宙双折射", "B 模"],
        "caption": "偏振角整体旋转会把 E 模泄漏到 B 模，并产生 EB 相关。这个信号的解释依赖绝对偏振角标定和前景偏振模型。",
    },
    {
        "chapter": 17,
        "filename": "ch17_entanglement_resources.pdf",
        "section_keywords": ["纠缠", "量子网络", "存储"],
        "caption": "量子网络望远镜的两个基本资源标度：纠缠分发率需要跟上有效光子率，量子存储时间至少要覆盖基线对应的光行时。",
    },
    {
        "chapter": 17,
        "filename": "ch17_fidelity_distance.pdf",
        "section_keywords": ["保真度", "频率转换", "链路"],
        "caption": "链路损耗和存储退相干共同决定长基线量子网络的有效保真度。即使光子率足够，高损耗也会把可用纠缠率压到不可行区域。",
    },
    {
        "chapter": 17,
        "filename": "ch17_network_parameter_space.pdf",
        "section_keywords": ["量子网络望远镜", "资源", "路线"],
        "caption": "基线、纠缠率和存储时间构成量子网络望远镜的资源空间。近期实验更接近短基线和低光子率角落，天文应用需要同时推进多个轴。",
    },
    {
        "chapter": 18,
        "filename": "ch18_photon_rate_magnitude.pdf",
        "section_keywords": ["光子率", "星等", "望远镜面积"],
        "caption": "AB 星等通过 10 的负 0.4m 次方快速压低光子率。望远镜面积和效率只能线性补偿，因此目标亮度是可行性估算的第一道门槛。",
    },
    {
        "chapter": 18,
        "filename": "ch18_snr_heatmap.pdf",
        "section_keywords": ["信噪比", "误差预算", "积分时间"],
        "caption": "强度相关信噪比随光子率和积分时间增加而提高。图中的等值线显示，提高时间分辨率以外，目标亮度和累计时间同样控制检出能力。",
    },
    {
        "chapter": 18,
        "filename": "ch18_error_budget.pdf",
        "section_keywords": ["误差预算", "系统误差", "可行性"],
        "caption": "误差预算把统计噪声、背景、时间标定和偏振标定放在同一尺度上。总误差通常由最大的几项主导，改进仪器时应先压低主导项。",
    },
    {
        "chapter": 19,
        "filename": "ch19_science_case_feasibility.pdf",
        "section_keywords": ["科学案例", "优先级", "第一代"],
        "caption": "第一代科学案例可以放在角尺度和光子率平面中比较。右上区域更适合早期实验，左下区域通常需要更长积分、更大阵列或新的量子资源。",
    },
    {
        "chapter": 19,
        "filename": "ch19_priority_matrix.pdf",
        "section_keywords": ["优先级", "路线", "科学案例"],
        "caption": "科学价值、技术成熟度和系统误差风险给出项目优先级矩阵。高价值但低成熟度的问题适合研究计划，高成熟度且风险低的问题适合作为第一代验证。",
    },
    {
        "chapter": 20,
        "filename": "ch20_hbt_lab_histogram.pdf",
        "section_keywords": ["教学实验", "HBT", "事件表"],
        "caption": "桌面 HBT 实验比较同时时间轴符合直方图和 time-shift 背景，并把零延迟峰归一化为 g2 延迟曲线。",
    },
    {
        "chapter": 20,
        "filename": "ch20_event_table_simulation.pdf",
        "section_keywords": ["事件表模拟", "Python", "实验"],
        "caption": "非齐次 Poisson 事件表保留到达时间、等效波长通道和质量标记，随后才投影成光变曲线或筛选后的计数率。",
    },
    {
        "chapter": 20,
        "filename": "ch20_uniform_disk_fit.pdf",
        "section_keywords": ["均匀圆盘", "角直径", "可见度"],
        "caption": "均匀圆盘强度干涉拟合把基线上的可见度平方点转成角直径后验，第一零点附近的点对直径最敏感。",
    },
    {
        "chapter": 20,
        "filename": "ch20_binary_visibility.pdf",
        "section_keywords": ["双星", "可见度", "轨道"],
        "caption": "双星可见度练习显示通量比如何控制振荡深度，以及轨道投影如何改变固定基线上的可见度平方。",
    },
    {
        "chapter": 20,
        "filename": "ch20_correlator_scaling.pdf",
        "section_keywords": ["相关器", "数据率", "基线"],
        "caption": "多望远镜相关器标度显示基线数随望远镜数二次增长，数据率随时间 bin 变窄和光谱通道增多而上升。",
    },
    {
        "chapter": 20,
        "filename": "ch20_spade_exercise.pdf",
        "section_keywords": ["Rayleigh", "SPADE", "计算实验"],
        "caption": "SPADE 计算实验比较直接成像和模式排序在小分离处的 Fisher 信息，并显示 Hermite-Gaussian 模式概率。",
    },
    {
        "chapter": 20,
        "filename": "ch20_typeia_distance_posterior.pdf",
        "section_keywords": ["Type Ia", "距离", "角半径"],
        "caption": "Type Ia 超新星 toy model 把速度模型给出的物理半径和强度干涉角半径合成角直径距离后验。",
    },
    {
        "chapter": 21,
        "filename": "ch21_g2_scaling_mistake.pdf",
        "section_keywords": ["误区", "光子", "g"],
        "caption": "时间 bin、滤光片带宽和有效模式数共同稀释热光聚束峰，宽带可见光很容易落到系统误差地板以下。",
    },
    {
        "chapter": 21,
        "filename": "ch21_calibration_artifacts.pdf",
        "section_keywords": ["校准", "串扰", "系统误差"],
        "caption": "电子串扰和校准残差可以比天体聚束峰更大，积分时间只能压低统计误差，不能自动消除系统误差地板。",
    },
    {
        "chapter": 21,
        "filename": "ch21_phase_loss.pdf",
        "section_keywords": ["相位", "成像", "可见度"],
        "caption": "只测可见度平方会留下镜像退化；同一可见度平方可以对应相位符号相反的天空亮度。",
    },
    {
        "chapter": 21,
        "filename": "ch21_superresolution_budget.pdf",
        "section_keywords": ["超分辨", "SPADE", "光子数"],
        "caption": "模式排序能降低小分离估计的统计误差，但光子数、模式串扰和质心误差仍然限制量子超分辨。",
    },
    {
        "chapter": 21,
        "filename": "ch21_maser_mixed_statistics.pdf",
        "section_keywords": ["maser", "laser", "统计"],
        "caption": "天体 maser/laser 候选的 g2 由窄线通量分数、热背景、强度噪声和谱线宽度共同决定。",
    },
    {
        "chapter": 21,
        "filename": "ch21_nonpoisson_diagnostics.pdf",
        "section_keywords": ["非 Poisson", "Fano", "仪器"],
        "caption": "变源、死时间和 afterpulsing 都能造成非 Poisson 统计，但它们在 Fano 因子和短延迟相关中留下不同形状。",
    },
    {
        "chapter": 21,
        "filename": "ch21_poisson_false_alarm.pdf",
        "section_keywords": ["Poisson", "新物理", "误区"],
        "caption": "单个 Poisson 尾部事件在大量 trial 中会变常见，事件表搜索必须报告全局假警报概率。",
    },
    {
        "chapter": 22,
        "filename": "ch22_roadmap_trade_space.pdf",
        "section_keywords": ["路线", "研究计划", "白皮书"],
        "caption": "路线图把技术成熟度、科学回报、成本和风险放在同一平面中，帮助区分近期 proposal 和远期路径验证。",
    },
    {
        "chapter": 22,
        "filename": "ch22_data_product_stack.pdf",
        "section_keywords": ["数据产品", "事件表", "归档"],
        "caption": "数据产品链从事件表经过相关函数和可见度进入似然、后验和公开归档，proposal 应逐项说明交付物。",
    },
    {
        "chapter": 22,
        "filename": "ch22_program_timeline.pdf",
        "section_keywords": ["2026", "2030", "研究计划"],
        "caption": "阶段性时间线从课程 HBT、探测器和恒星样本推进到多通道相关、瞬变跟进、本地模式排序和量子网络 pathfinder。",
    },
    {
        "chapter": 22,
        "filename": "ch22_milestone_gates.pdf",
        "section_keywords": ["里程碑", "readiness", "验收"],
        "caption": "里程碑门槛矩阵把光子率、计时、校准、pipeline 和科学样本分别量化，避免用单一硬件指标代表 readiness。",
    },
    {
        "chapter": 22,
        "filename": "ch22_risk_register.pdf",
        "section_keywords": ["风险", "proposal", "失败判据"],
        "caption": "风险登记图按概率和影响排列目标过暗、计时漂移、零基线偏差、选择效应、模型退化、数据量和网络损耗。",
    },
]


def figures_for_chapter(chapter: int | str) -> list[dict[str, object]]:
    chapter_number = int(chapter)
    return [figure for figure in FIGURES if int(figure["chapter"]) == chapter_number]


def figures_by_chapter() -> dict[int, list[dict[str, object]]]:
    grouped: dict[int, list[dict[str, object]]] = {}
    for figure in FIGURES:
        grouped.setdefault(int(figure["chapter"]), []).append(figure)
    return grouped
