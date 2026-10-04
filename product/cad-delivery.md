# 吊牌 CAD 交付与检查记录

## 当前交付
- 最终版本：relief-pendant，build 3。
- STEP：`manufacturing/relief-pendant/releases/export-ec061807783ffd047f7894b9fe56facf/model.step`。
- 导出记录：同目录 `receipt.json`。
- STEP SHA-256：`ec2d5638bae39cc1818edbaf265c8e5e64752f5e354fb90c9dec629d44eea08e`。
- 参数化源码：`design/relief-pendant/source/`；约束和零件表：`product/constraints.json`、`product/bom.json`。

## 本版要求和检查
用户标注 #1 的中部 43 × 4 mm 胶囊长条为下凹结构，不改变下方 Select effort 底块或其他图案。默认槽深为可调的 0.4 mm，槽底 Z=2.6 mm，剩余底厚 2.6 mm。

圆形按钮中心 (18,-1) mm、直径 4 mm、顶面 Z=3.8 mm 保持与 build 2 一致；按钮下方的同径材料柱连接槽底，避免悬空。源码保留所有原有参数，仅新增 pendant_slider_recess_depth；代码差异检查显示其他图案生成段未改变。构建断言检查了按钮直径及顶面高度、槽深范围和单实体连接。

- CAD 内核检查：有效实体，solidCount=1。
- 数值几何分析：50 × 34 × 3.8 mm，背面 Z=0，整体包络未变。
- 正视和斜视：确认长条凹槽边界、槽壁和槽底；圆形按钮仍在右侧凸起，文字与其余图案保持原布局。
- 独立复核：No P0 or P1 findings，review-3-095ac9a9-51d9-4db4-9518-863429561f28。
- 导出后 STEP 预览已刷新，CAD 状态 ready，未报告剩余诊断。

## 视觉证据
- 正视：`.work/cache/cad-workbench/designs/relief-pendant/observations/eb8c8e6cb59870d5ea70e56008bc17ada36f3162948141df440bb93b146e27c3/look-941337f5ef2242ef74991668/workbench_top.png`
- 斜视：`.work/cache/cad-workbench/designs/relief-pendant/observations/eb8c8e6cb59870d5ea70e56008bc17ada36f3162948141df440bb93b146e27c3/look-941337f5ef2242ef74991668/workbench_iso.png`

## 使用限制
单一融合实体的几何交付，预览为单色，非多材料生产数据。制造工艺、材料、打印细节和吊耳承载性能未验证；未生成切片或 G-code。
