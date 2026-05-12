# 三人成行队_系统设计说明书

---

## 1. 引言

### 1.1 编写目的

本文档用于说明“三人成行队”实验教学管理系统项目在系统设计阶段的总体设计方案，重点描述系统架构、功能划分、业务流程、UML 设计、前后端结构及部署思路，为后续编码实现、联调测试和团队协作提供统一依据。

### 1.2 项目背景

在第一次团队作业中，团队已完成项目选题、需求分析和系统规划。本阶段工作聚焦于将需求转化为可执行的软件设计方案，形成完整的原型设计与概要设计成果。项目目标是构建一个面向实验课程教学管理的综合平台，支持教师组织实验、学生执行实验步骤、课堂签到、课堂小测、成绩管理、数据导入和资源管理等功能。

### 1.3 术语与缩写

| 术语 | 含义 |
| --- | --- |
| UML | 统一建模语言，用于表达系统结构与行为 |
| JWT | JSON Web Token，用于前后端分离场景下的身份认证 |
| API | 应用程序编程接口 |
| ER 图 | 实体联系图，用于数据库设计 |
| Mapper | 数据访问层接口 |
| DTO | 数据传输对象 |
| VO | 视图对象 |

### 1.4 参考资料

1. `signLab` 项目代码仓库
2. `newLab` 前端原型仓库
3. `md/旧项目文档.md`
4. `md/班级和学生班级功能文档.md`
5. `md/批量导入用户文档.md`
6. 课程作业要求页面

---

## 2. 系统概述

### 2.1 系统目标

本系统面向高校实验课程教学场景，目标是实现教学组织数字化、实验过程结构化和学习评价可追踪化。系统以课程、班级、实验、实验步骤和课堂小测为业务核心，打通教师组织教学、学生完成实验、系统记录过程、教师统计结果的完整链路。

### 2.2 用户角色

系统主要用户角色如下：

1. **学生**
   - 参与课程学习
   - 完成扫码签到
   - 查看实验与步骤
   - 提交实验数据与附件
   - 参与课堂小测
   - 查询成绩与考勤

2. **教师**
   - 维护课程与班级
   - 创建实验与步骤
   - 管理题库、视频和课堂小测
   - 查看学生过程数据与成绩统计
   - 批量导入教学数据

3. **管理员**
   - 协助维护用户账号
   - 进行密码重置与基础数据维护

4. **外部系统**
   - 微信平台：用于登录授权与消息通知

### 2.3 设计原则

- **贴合教学业务**：设计围绕实验教学真实流程展开。
- **分层清晰**：前端、控制、业务、数据访问与存储职责清楚。
- **角色隔离**：通过统一认证与权限控制区分不同用户能力。
- **可扩展**：实验步骤、小测、数据采集和资源管理均可继续扩展。
- **与实现一致**：本设计说明尽量严格对应现有仓库结构和代码实现。

---

## 3. 系统总体架构设计

### 3.1 总体架构

系统采用前后端分离架构，可划分为四层：

1. **表示层**
   - Vue 3 前端页面
   - 登录页
   - 学生端页面
   - 教师端后台页面

2. **控制层**
   - Spring Boot Controller
   - 负责请求接收、参数校验、响应封装

3. **业务层**
   - Service 服务类
   - 负责认证、课程管理、实验步骤处理、课堂小测、成绩统计等业务逻辑

4. **数据层**
   - MyBatis Plus Mapper
   - MySQL 数据库
   - SQL 脚本与实体映射

### 3.2 架构特点

- 前端通过路由自动生成与页面分模块组织，提高页面扩展能力；
- 后端通过 `Controller + Service + Mapper + Entity` 分层实现业务闭环；
- 认证采用 JWT，无需服务端保存会话；
- 角色控制通过注解和 AOP 切面统一处理；
- 数据库结构既支持自动建表，也支持 SQL 脚本迁移；
- 文件资源与业务数据分离管理，便于后续部署和扩容。

### 3.3 技术架构

#### 前端技术

| 技术 | 作用 |
| --- | --- |
| Vue 3 | 页面开发框架 |
| TypeScript | 类型安全与可维护性 |
| Vite | 前端构建工具 |
| Vue Router | 页面路由管理 |
| PrimeVue | 教师端界面组件 |

#### 后端技术

| 技术 | 作用 |
| --- | --- |
| Spring Boot 3 | 后端主框架 |
| MyBatis Plus | 数据访问框架 |
| MySQL | 关系数据库 |
| JWT | 令牌认证 |
| AutoTable | 自动建表与实体映射 |
| EasyExcel / POI | Excel 与文档处理 |
| ZXing | 二维码生成 |

---

## 4. 功能模块设计

### 4.1 认证与用户管理模块

#### 功能说明

该模块负责系统的统一登录入口、身份认证、密码维护和微信绑定，是全系统访问控制的基础。

#### 主要功能

- 用户名密码登录
- 首次登录设置密码
- 管理员重置密码
- 微信绑定状态查询
- 微信登录与解绑
- 用户状态查询

#### 相关实现位置

- `src/main/java/com/example/demo/controller/AuthController.java`
- `src/main/java/com/example/demo/service/AuthService.java`
- `src/main/java/com/example/demo/pojo/entity/User.java`

### 4.2 班级与课程管理模块

#### 功能说明

该模块负责维护教学组织基础数据，是实验教学任务发布和学生归属关系建立的基础。

#### 主要功能

- 班级创建与修改
- 课程创建与查询
- 学生与班级关系绑定
- 批量导入用户、班级、课程与关联关系
- 教师查看课程与班级统计

#### 相关实现位置

- `controller/teacher/ClassController.java`
- `controller/teacher/CourseController.java`
- `controller/ExcelTestController.java`
- `service/ClassService.java`
- `service/CourseService.java`
- `service/StudentClassRelationService.java`

### 4.3 实验与步骤管理模块

#### 功能说明

该模块是项目的核心业务模块，负责实验任务创建、步骤配置和班级实验组织。实验步骤支持多种任务类型，支撑教学过程化管理。

#### 主要功能

- 创建实验
- 为实验配置步骤
- 按班级分配实验
- 设置步骤顺序、开始偏移、持续时间
- 支持视频学习、数据收集、题库答题与限时小测

#### 相关实现位置

- `controller/teacher/TeacherExperimentController.java`
- `controller/teacher/TeacherProcedureController.java`
- `controller/teacher/TeacherProcedureCreationController.java`
- `service/ExperimentService.java`
- `service/ExperimentalProcedureService.java`
- `pojo/entity/Experiment.java`
- `pojo/entity/ExperimentalProcedure.java`

### 4.4 学生实验执行模块

#### 功能说明

该模块面向学生，负责实验过程执行，是学生完成课堂任务的主要入口。

#### 主要功能

- 查询课程场次
- 查询实验步骤提交状态
- 查看未完成步骤详情
- 查看已完成步骤详情
- 标记视频学习完成
- 提交题库作答
- 提交数据采集内容与附件

#### 相关实现位置

- `controller/student/StudentProcedureController.java`
- `service/StudentProcedureQueryService.java`
- `service/StudentProcedureCompletionService.java`
- `service/StudentProcedureSubmissionService.java`
- `service/StudentExperimentalProcedureService.java`

### 4.5 课堂小测与题库模块

#### 功能说明

该模块用于支撑课堂互动与过程性评价，教师可以配置题目与标签并发起课堂小测，学生按实验或课堂任务进行作答。

#### 主要功能

- 创建题目与标签
- 管理题目标签映射
- 创建过程题库配置
- 发起课堂小测
- 学生提交课堂小测答案
- 教师查看结果统计与得分

#### 相关实现位置

- `controller/teacher/TeacherTopicController.java`
- `controller/teacher/TeacherTagController.java`
- `controller/teacher/TeacherClassroomQuizController.java`
- `controller/student/StudentClassroomQuizController.java`
- `pojo/entity/Topic.java`
- `pojo/entity/Tag.java`
- `pojo/entity/ClassroomQuiz.java`
- `pojo/entity/ClassroomQuizAnswer.java`

### 4.6 成绩与统计模块

#### 功能说明

该模块用于汇总学生在课程、实验、课堂小测中的结果数据，支撑教师教学评价和学生自我查看。

#### 主要功能

- 课程成绩查询
- 成绩录入与计算
- 考勤统计
- 课堂小测结果统计
- 学生个人成绩查询

#### 相关实现位置

- `controller/student/StudentGradeController.java`
- `controller/teacher/TeacherGradeController.java`
- `controller/student/StudentAttendanceController.java`
- `controller/teacher/TeacherAttendanceController.java`
- `service/CourseGradeService.java`
- `service/GradeCalculationService.java`
- `service/AttendanceRecordService.java`

### 4.7 资源与辅助功能模块

#### 功能说明

该模块为系统提供文件、视频、二维码、微信通知和导出能力，提升系统完整性与实用性。

#### 主要功能

- 实验视频上传与查看
- 文件下载
- 二维码签到
- 微信消息提醒
- 数据导出

#### 相关实现位置

- `controller/QrController.java`
- `controller/DownloadController.java`
- `controller/WeChatController.java`
- `controller/teacher/TeacherVideoController.java`
- `controller/teacher/TeacherExportController.java`
- `service/QrService.java`
- `service/DownloadService.java`
- `service/VideoService.java`
- `service/WeChatService.java`

---

## 5. 业务流程设计

### 5.1 用户登录流程

1. 用户进入登录页；
2. 输入学号或工号以及密码；
3. 前端调用 `/api/auth/login`；
4. 后端验证用户信息；
5. 验证通过后返回用户信息和 JWT；
6. 前端根据角色将用户路由到学生端或教师端首页。

### 5.2 教师创建实验流程

1. 教师登录系统；
2. 进入课程或实验管理模块；
3. 创建实验基础信息；
4. 配置实验步骤；
5. 为步骤设置具体类型与资源；
6. 绑定班级实验；
7. 学生可在课程场次中看到对应实验。

### 5.3 学生完成实验步骤流程

1. 学生查看课程场次；
2. 进入某次实验；
3. 系统返回实验步骤列表与状态；
4. 学生按步骤执行视频学习、数据填写或题目作答；
5. 后端记录完成结果与附件；
6. 系统刷新步骤完成状态并用于后续成绩统计。

### 5.4 课堂小测流程

1. 教师在实验过程中发起课堂小测；
2. 学生获取小测任务并作答；
3. 系统记录答题结果；
4. 后端统计得分和正确率；
5. 教师在后台查看结果并用于评价。

### 5.5 批量导入流程

1. 教师准备规定格式的 Excel 文件；
2. 调用批量导入接口；
3. 后端逐条校验、分批写入数据库；
4. 返回导入统计结果；
5. 教师查看日志与数据状态。

---

## 6. UML 设计说明

### 6.1 用例图设计

#### 参与者

- 学生
- 教师
- 管理员
- 微信平台

#### 主要用例

**学生用例：**
- 登录
- 查看课程
- 查询实验步骤
- 提交实验数据
- 上传附件
- 参加课堂小测
- 查看成绩与考勤

**教师用例：**
- 登录
- 创建班级
- 创建课程
- 创建实验
- 配置实验步骤
- 发布课堂小测
- 查看统计
- 批量导入数据

**管理员用例：**
- 重置密码
- 维护用户数据

### 6.2 活动图设计

#### 学生执行实验活动图

开始 → 登录 → 查看课程 → 选择实验 → 查看步骤 → 判断步骤类型 → 执行对应任务 → 提交结果 → 系统保存 → 结束

#### 教师发布实验活动图

开始 → 登录 → 管理课程与班级 → 创建实验 → 配置步骤 → 绑定实验与班级 → 发布 → 学生可见 → 结束

### 6.3 类图设计

建议绘制的核心类包括：

- `User`
- `Class`
- `Course`
- `StudentClassRelation`
- `Experiment`
- `ExperimentalProcedure`
- `DataCollection`
- `ProcedureTopic`
- `Topic`
- `Tag`
- `ClassroomQuiz`
- `ClassroomQuizAnswer`
- `CourseGrade`
- `VideoFile`

类关系说明：

- 一个用户可以属于多个班级关系；
- 一个课程可关联多个实验；
- 一个实验包含多个步骤；
- 一个步骤按照类型可关联视频、数据收集或题库；
- 一个课堂小测对应多个学生答案；
- 一个题目可拥有多个标签。

### 6.4 时序图设计

#### 登录时序图

用户 → 登录页 → AuthController → AuthService → User / JWT 工具 → 返回结果 → 前端路由跳转

#### 步骤提交时序图

学生页面 → StudentProcedureController → StudentProcedureSubmissionService / CompletionService → Mapper / 数据库 → 返回提交状态 → 页面更新

### 6.5 协作图设计

协作图建议围绕以下对象绘制：

- 登录页组件、认证控制器、认证服务、用户实体、JWT 工具；
- 学生步骤页、步骤控制器、步骤查询服务、步骤提交服务、附件实体、数据库；
- 教师总览页、课程控制器、实验控制器、课堂小测控制器、统计服务。

---

## 7. 前后端交互设计

### 7.1 前端页面结构

根据 `newLab` 项目页面结构，系统页面主要包括：

- `login.page.vue`：登录页
- `student/index.page.vue`：学生课程首页
- `student/courses/[courseId]/index.page.vue`：课程详情
- `student/experiments/[experimentId].page.vue`：实验详情
- `student/experiment-steps/[stepId].page.vue`：实验步骤页
- `student/classroom-quiz/index.page.vue`：课堂小测
- `teacher/overview/index.page.vue`：教师总览
- `teacher/courses/index.page.vue`：课程管理
- `teacher/classes/index.page.vue`：班级管理
- `teacher/experiments/index.page.vue`：实验管理
- `teacher/topics/index.page.vue`：题库管理
- `teacher/videos/index.page.vue`：视频管理

### 7.2 前后端接口配合方式

- 前端通过统一路由进入不同角色页面；
- 请求通过 Token 携带身份信息；
- 后端返回统一响应结构；
- 学生端重点调用课程、实验、步骤、小测、成绩相关接口；
- 教师端重点调用课程、班级、实验、题库、导入和统计相关接口。

---

## 8. 部署与运行环境设计

### 8.1 运行环境

| 类别 | 要求 |
| --- | --- |
| JDK | Java 17 |
| 构建工具 | Maven |
| 数据库 | MySQL 8.0 及以上 |
| 前端运行环境 | Node.js 对应 Vite 开发环境 |
| 操作系统 | Windows / Linux |

### 8.2 配置项说明

系统通过环境变量和 `application.yml` 进行配置，主要包括：

- 数据库连接信息
- JWT 密钥与过期时间
- 文件上传路径
- 服务器端口与地址
- 微信平台参数

### 8.3 部署建议

- 前端可部署为静态站点；
- 后端以 Spring Boot 服务部署；
- 数据库独立部署；
- 上传文件目录与数据库目录分离；
- 可由 Nginx 进行统一反向代理。

---

## 9. 设计约束与风险分析

### 9.1 设计约束

- 系统必须支持教师、学生、管理员三类角色；
- 实验步骤需要支持多类型配置；
- 设计需兼顾移动端学习场景与后台管理场景；
- 数据模型需支撑后续评分和过程追踪；
- 前后端设计需与现有代码结构一致。

### 9.2 风险分析

- 若实验步骤配置复杂度继续提升，前后端联调成本会增加；
- 微信登录与消息通知依赖外部平台，存在环境配置复杂问题；
- 数据导入场景字段较多，若模板不一致会影响数据质量；
- 若缺少图形化 UML 输出，文字设计说明的可视化程度会不足。

### 9.3 优化方向

- 后续可补充统一接口文档；
- 可增加流程图、类图和时序图图片版本；
- 可进一步完善成绩计算规则与异常处理说明；
- 可补充管理员后台模块设计。

---

## 10. 结论

本说明书从系统目标、总体架构、模块划分、业务流程、UML 设计、前后端交互和部署思路等方面，对 SignLab 实验教学管理系统进行了概要设计。整体设计已经形成以课程组织、实验执行、课堂小测和过程性评价为主线的系统方案，能够支撑后续开发工作有序推进，并为团队成员分工协作和功能落地提供统一设计基线。
