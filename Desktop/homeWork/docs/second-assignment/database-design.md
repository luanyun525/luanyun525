# 三人成行队_数据库设计说明书

---

## 1. 引言

### 1.1 编写目的

本文档用于说明 SignLab 实验教学管理系统的数据库设计方案，重点描述业务实体、ER 关系、关系模型、主表结构、约束规则、索引策略以及对象关系映射，为后续数据库实现、后端编码、数据联调与系统维护提供统一依据。

### 1.2 设计目标

数据库设计需要满足以下目标：

1. 支撑学生、教师、管理员三类角色的基础数据管理；
2. 支撑课程、班级、实验、实验步骤、小测与成绩等核心教学业务；
3. 支撑实验过程数据留痕与过程性评价；
4. 支撑批量导入、过程查询、统计分析等高频场景；
5. 与现有后端实体类和 SQL 脚本保持一致。

### 1.3 设计依据

本数据库设计主要依据以下内容整理：

- `src/main/resources/application.yml`
- `src/main/resources/sql/classroom_quiz.sql`
- `src/main/resources/sql/timed_quiz_procedure_migration.sql`
- `src/main/java/com/example/demo/pojo/entity/*.java`
- `md/批量导入用户文档.md`
- `md/旧项目文档.md`

---

## 2. 数据库总体设计

### 2.1 数据库类型

系统采用 **MySQL** 作为关系数据库，适合结构化教学业务数据存储、事务处理和关系查询。

### 2.2 数据库命名与设计风格

- 数据表采用小写下划线命名；
- 实体字段命名与 Java 对象基本保持驼峰映射关系；
- 通用字段包括创建时间、更新时间与逻辑删除标记；
- 通过唯一索引、普通索引和关联键优化查询性能；
- 通过 AutoTable 注解与 SQL 脚本共同维护数据库结构。

### 2.3 数据库分层思路

数据库按业务语义大致分为三类：

1. **基础主数据层**
   - 用户、班级、课程、学生班级关系

2. **教学过程层**
   - 实验、班级实验、实验步骤、数据收集、视频、题库、标签

3. **评价与结果层**
   - 课堂小测、课堂小测答案、课程成绩、学生步骤提交、附件等

---

## 3. 业务实体分析

### 3.1 用户实体

用户实体用于表示系统中的学生、教师和管理员，包含账号、姓名、角色、密码状态、院系、专业以及微信绑定信息。

### 3.2 班级实体

班级实体用于表示一个教学班，是课程组织和学生归属关系的基础。

### 3.3 课程实体

课程实体用于表示实验教学中的课程信息，与教师和学生班级存在关联，是实验活动的时间与组织载体。

### 3.4 学生班级关系实体

用于建立学生与班级之间的多对一关系，便于课程查询、班级绑定和跨流程统计。

### 3.5 实验实体

实验实体描述某门课程下的实验任务本体，是实验步骤和课堂小测的上层组织对象。

### 3.6 实验步骤实体

实验步骤实体描述学生在实验过程中需要逐步完成的任务，是系统最关键的过程性业务对象。步骤支持视频观看、数据收集、题库答题和限时答题等不同类型。

### 3.7 数据收集实体

数据收集实体用于描述实验过程中需要学生填写或提交的数据项，可与附件上传配合使用。

### 3.8 题目与标签实体

题目实体存放题库题目，标签实体用于给题目分类，通过映射表建立多对多关系，支撑题库复用和课堂小测配置。

### 3.9 课堂小测实体

课堂小测实体用于描述教师发起的一次小测活动，答案实体用于记录每位学生对应小测的作答情况与成绩。

### 3.10 成绩与资源实体

成绩实体用于记录课程或实验相关成绩；视频与附件实体用于管理过程资源和提交文件。

---

## 4. ER 图设计说明

### 4.1 核心实体关系

系统 ER 关系可概括如下：

- 一个 `User` 可对应多个 `StudentClassRelation` 记录；
- 一个 `Class` 可包含多个学生；
- 一个 `Course` 可由一个教师负责，并与多个实验场次有关；
- 一个 `Experiment` 可包含多个 `ExperimentalProcedure`；
- 一个 `ExperimentalProcedure` 可按类型关联 `VideoFile`、`DataCollection`、`ProcedureTopic` 或 `TimedQuizProcedure`；
- 一个 `ClassroomQuiz` 对应多个 `ClassroomQuizAnswer`；
- 一个 `Topic` 可关联多个 `Tag`，一个 `Tag` 也可关联多个 `Topic`；
- 一个学生可在多个实验步骤中产生多个步骤提交记录与附件记录。

### 4.2 建议绘制的 ER 图对象

建议在最终 PDF 中将以下对象纳入 ER 图：

- `users`
- `classes`
- `student_class_relations`
- `courses`
- `experiments`
- `class_experiments`
- `experiment_procedure`
- `data_collection`
- `topics`
- `tags`
- `topic_tag_map`
- `procedure_topic`
- `classroom_quiz`
- `classroom_quiz_answer`
- `course_grades`
- `video_files`

---

## 5. 关系数据模型设计

### 5.1 主要关系模式

以下给出核心关系模型的文字表达：

1. `users(id, username, name, password, role, password_set, department, major, wx_openid, wx_unionid, wx_nickname, wx_avatar, wx_bind_time, create_time, update_time, is_deleted)`
2. `classes(id, class_code, class_name, student_count, verification_code, create_time, update_time, is_deleted)`
3. `student_class_relations(id, student_username, class_code, bind_time, is_deleted)`
4. `courses(id, course_id, course_name, teacher_username, create_time, update_time, is_deleted)`
5. `experiments(id, experiment_name, course_id, remark, create_time, update_time, is_deleted)`
6. `experiment_procedure(id, experiment_id, number, is_skip, proportion, type, remark, video_id, data_collection_id, procedure_topic_id, timed_quiz_id, offset_minutes, duration_minutes, is_deleted)`
7. `data_collection(id, ...)`
8. `topics(id, ...)`
9. `tags(id, ...)`
10. `topic_tag_map(id, topic_id, tag_id, ...)`
11. `procedure_topic(id, ...)`
12. `classroom_quiz(id, class_experiment_id, procedure_topic_id, quiz_title, quiz_description, quiz_time_limit, status, start_time, end_time, created_by, created_time)`
13. `classroom_quiz_answer(id, classroom_quiz_id, student_username, class_code, answer, score, is_correct, submission_time)`
14. `course_grades(id, student_username, course_id, grade, teacher_username, teacher_comment, ...)`
15. `video_files(id, ...)`

### 5.2 关系模型特点

- 采用用户、课程、班级作为基础主线；
- 采用实验与步骤建模表达过程型教学任务；
- 采用题库、小测、成绩建模表达评价体系；
- 采用映射表表达题目与标签等多对多关系；
- 采用逻辑删除字段保留业务痕迹与历史数据。

---

## 6. 核心数据表设计

### 6.1 用户表 `users`

#### 设计目的

存储学生、教师和管理员的统一账户信息，并为微信绑定与身份认证提供支持。

#### 关键字段

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | bigint | 主键 |
| username | varchar(50) | 用户名，学号或工号，唯一 |
| name | varchar(100) | 姓名 |
| password | varchar(255) | 加密密码 |
| role | enum | 角色：student / teacher / admin |
| password_set | tinyint | 是否已设置密码 |
| department | varchar(100) | 院系 |
| major | varchar(100) | 专业 |
| wx_openid | varchar(100) | 微信 OpenID |
| wx_unionid | varchar(100) | 微信 UnionID |
| wx_nickname | varchar(100) | 微信昵称 |
| wx_avatar | varchar(500) | 微信头像 |
| wx_bind_time | datetime | 微信绑定时间 |
| create_time | datetime | 创建时间 |
| update_time | datetime | 更新时间 |
| is_deleted | tinyint | 逻辑删除标记 |

#### 约束与索引

- 主键：`id`
- 唯一索引：`username`
- 唯一索引：`wx_openid`
- 普通索引：`role`、`department`、`major`、`wx_unionid`

### 6.2 课程表 `courses`

#### 设计目的

存储课程基本信息，为课程展示、实验组织和成绩管理提供主索引。

#### 关键字段

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | bigint | 主键 |
| course_id | varchar(20) | 课程编号，唯一 |
| course_name | varchar(200) | 课程名称 |
| teacher_username | varchar(50) | 任课教师用户名 |
| create_time | datetime | 创建时间 |
| update_time | datetime | 更新时间 |
| is_deleted | tinyint | 逻辑删除标记 |

#### 约束与索引

- 主键：`id`
- 唯一索引：`course_id`
- 普通索引：`teacher_username`

### 6.3 实验步骤表 `experiment_procedure`

#### 设计目的

表达实验内部的执行步骤，是实验业务中最关键的数据表之一。

#### 关键字段

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | bigint | 主键 |
| experiment_id | bigint | 所属实验 ID |
| number | int | 步骤顺序 |
| is_skip | bit | 是否允许跳过 |
| proportion | int | 步骤分值占比 |
| type | int | 步骤类型 |
| remark | text | 步骤描述 |
| video_id | bigint | 视频资源 ID |
| data_collection_id | bigint | 数据收集配置 ID |
| procedure_topic_id | bigint | 题库配置 ID |
| timed_quiz_id | bigint | 限时答题配置 ID |
| offset_minutes | int | 相对实验开始时间的偏移 |
| duration_minutes | int | 持续时间 |
| is_deleted | bit | 逻辑删除标记 |

#### 类型说明

- `1`：观看视频
- `2`：数据收集
- `3`：题库答题
- `5`：限时答题

#### 设计特点

- 同一张步骤表支撑多种业务类型；
- 支持时间窗控制；
- 支持分值占比配置；
- 便于后续扩展新的步骤类型。

### 6.4 课堂小测表 `classroom_quiz`

#### 设计目的

记录教师发起的课堂小测活动，是课堂互动与过程性评价的重要载体。

#### 关键字段

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | bigint | 主键 |
| class_experiment_id | bigint | 班级实验 ID |
| procedure_topic_id | bigint | 题库配置 ID |
| quiz_title | varchar(255) | 小测标题 |
| quiz_description | text | 小测描述 |
| quiz_time_limit | int | 答题时限，单位分钟 |
| status | tinyint | 状态：未开始 / 进行中 / 已结束 |
| start_time | datetime | 开始时间 |
| end_time | datetime | 结束时间 |
| created_by | varchar(50) | 创建教师用户名 |
| created_time | datetime | 创建时间 |

#### 索引设计

- 主键：`id`
- 普通索引：`class_experiment_id`
- 普通索引：`procedure_topic_id`
- 普通索引：`created_by`

### 6.5 课堂小测答案表 `classroom_quiz_answer`

#### 设计目的

记录学生对课堂小测的答题情况与结果，用于成绩分析和结果展示。

#### 关键字段

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | bigint | 主键 |
| classroom_quiz_id | bigint | 所属小测 ID |
| student_username | varchar(50) | 学生用户名 |
| class_code | varchar(20) | 班级编号 |
| answer | text | JSON 格式答案 |
| score | decimal(5,2) | 得分 |
| is_correct | tinyint | 是否全部正确 |
| submission_time | datetime | 提交时间 |

#### 约束与索引

- 主键：`id`
- 唯一约束：`(classroom_quiz_id, student_username)`
- 普通索引：`student_username`
- 普通索引：`class_code`

### 6.6 课程成绩表 `course_grades`

#### 设计目的

记录教师对学生在课程维度下的成绩评价，支撑课程成绩查询与统计。

#### 关键字段

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | bigint | 主键 |
| student_username | varchar(50) | 学生学号 |
| course_id | varchar(50) | 课程编号 |
| grade | string / decimal | 成绩 |
| teacher_username | varchar(50) | 教师工号 |
| teacher_comment | varchar / text | 教师评语 |

---

## 7. 主外键与约束设计

### 7.1 主键设计

系统各核心表均采用自增主键 `id`，便于后续扩展与统一管理。

### 7.2 唯一约束设计

为防止重复数据和提高数据一致性，设计中采用如下唯一约束：

- `users.username`
- `users.wx_openid`
- `courses.course_id`
- `classroom_quiz_answer(classroom_quiz_id, student_username)`

### 7.3 业务约束设计

- 用户角色必须限定为学生、教师或管理员；
- 步骤类型必须在预设范围内；
- 小测状态必须符合生命周期约束；
- 同一学生对同一小测仅允许提交一次最终答卷；
- 大量业务表统一使用 `is_deleted` 实现逻辑删除。

### 7.4 时间与状态约束

- 步骤执行受 `offset_minutes` 与 `duration_minutes` 控制；
- 小测受 `start_time`、`end_time` 和 `status` 控制；
- 创建与更新时间字段用于保留过程记录。

---

## 8. 索引设计

### 8.1 索引目标

索引设计主要用于提升以下查询性能：

- 按用户名查询用户、成绩、答题记录；
- 按课程编号查询课程与实验；
- 按实验或班级实验查询小测；
- 按题库配置查询小测与步骤；
- 按角色或专业筛选用户。

### 8.2 主要索引场景

| 数据表 | 索引字段 | 目的 |
| --- | --- | --- |
| users | username | 登录与身份查找 |
| users | role | 角色筛选 |
| users | department / major | 用户筛选与统计 |
| courses | course_id | 课程唯一定位 |
| courses | teacher_username | 教师课程查询 |
| classroom_quiz | class_experiment_id | 查询某班级实验下的小测 |
| classroom_quiz_answer | student_username | 查询学生答题记录 |
| classroom_quiz_answer | class_code | 按班级统计结果 |

---

## 9. 对象关系映射设计

### 9.1 映射方式

系统使用 MyBatis Plus 结合注解完成实体与表的映射，核心模式包括：

- `@TableName`：指定表名
- `@TableId`：指定主键
- `@AutoTable`：支持自动建表
- `@TableIndex`：定义索引
- `@Column`：定义字段类型、注释、默认值与约束

### 9.2 映射示例

#### 用户实体映射

- Java 实体：`User`
- 数据表：`users`
- 关键映射：
  - `username` → 用户名
  - `role` → 角色
  - `wxOpenid` → 微信绑定字段
  - `isDeleted` → 逻辑删除标记

#### 课程实体映射

- Java 实体：`Course`
- 数据表：`courses`
- 关键映射：
  - `courseId` → 课程编号
  - `courseName` → 课程名称
  - `teacherUsername` → 任课教师工号

#### 实验步骤实体映射

- Java 实体：`ExperimentalProcedure`
- 数据表：`experiment_procedure`
- 关键映射：
  - `experimentId` → 所属实验
  - `Type` → 步骤类型
  - `videoId / dataCollectionId / procedureTopicId / timedQuizId` → 不同业务分支资源关联

### 9.3 映射特点

- 数据结构和后端对象模型耦合度高，便于开发和维护；
- 自动建表可降低初期表结构维护成本；
- SQL 脚本迁移补充了复杂业务结构的演进能力；
- 注解式映射使数据库语义在实体层面可直接阅读。

---

## 10. 数据导入与初始化设计

### 10.1 导入场景

系统支持通过 Excel 批量导入以下数据：

- 用户
- 班级
- 课程
- 学生班级关系
- 考勤记录
- 课程成绩
- 作业提交

### 10.2 导入特点

- 支持按模板字段顺序导入；
- 支持分批插入；
- 支持导入结果统计；
- 支持错误日志定位；
- 适合开学初或课程批量初始化场景。

### 10.3 初始化建议

推荐导入顺序：

1. 用户
2. 班级
3. 课程
4. 学生班级关系
5. 其他业务数据

---

## 11. 数据安全与完整性设计

### 11.1 安全性设计

- 密码采用加密存储；
- 用户认证通过 JWT 进行控制；
- 教师与学生操作受角色权限限制；
- 逻辑删除降低误删风险；
- 微信身份字段单独存储，便于绑定状态管理。

### 11.2 完整性设计

- 通过唯一约束防止关键业务重复；
- 通过映射字段保持对象与表的一致性；
- 通过步骤类型和时间窗口约束实验执行合法性；
- 通过小测答案唯一约束防止重复提交。

---

## 12. 设计总结

本数据库设计围绕“用户—课程—实验—步骤—小测—成绩”主线展开，能够完整支撑实验教学管理系统的主要业务需求。整体设计兼顾基础主数据、过程性业务数据与结果性评价数据，并与后端实体模型、导入流程和前端业务页面形成较好对应关系。后续只需在此基础上补充 ER 图图片、字段细化说明和必要的迁移脚本说明，即可形成可提交的数据库设计说明书正式版。
