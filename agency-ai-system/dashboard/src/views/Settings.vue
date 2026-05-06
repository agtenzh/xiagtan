<template>
  <div class="settings-container">
    <div class="page-header">
      <h2>系统设置</h2>
      <el-button type="primary" @click="saveSettings">
        <el-icon><Check /></el-icon>
        保存设置
      </el-button>
    </div>

    <el-tabs v-model="activeTab">
      <!-- 基本设置 -->
      <el-tab-pane label="基本设置" name="basic">
        <el-card>
          <template #header>
            <span>系统基本设置</span>
          </template>
          <el-form :model="basicSettings" label-width="120px">
            <el-form-item label="系统名称">
              <el-input v-model="basicSettings.app_name" />
            </el-form-item>
            <el-form-item label="系统描述">
              <el-input v-model="basicSettings.app_description" type="textarea" :rows="2" />
            </el-form-item>
            <el-form-item label="日志级别">
              <el-select v-model="basicSettings.log_level">
                <el-option label="DEBUG" value="DEBUG" />
                <el-option label="INFO" value="INFO" />
                <el-option label="WARNING" value="WARNING" />
                <el-option label="ERROR" value="ERROR" />
              </el-select>
            </el-form-item>
            <el-form-item label="语言">
              <el-select v-model="basicSettings.language">
                <el-option label="中文" value="zh-CN" />
                <el-option label="English" value="en-US" />
              </el-select>
            </el-form-item>
            <el-form-item label="时区">
              <el-select v-model="basicSettings.timezone">
                <el-option label="Asia/Shanghai" value="Asia/Shanghai" />
                <el-option label="America/New_York" value="America/New_York" />
                <el-option label="Europe/London" value="Europe/London" />
              </el-select>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 任务设置 -->
      <el-tab-pane label="任务设置" name="tasks">
        <el-card>
          <template #header>
            <span>任务配置</span>
          </template>
          <el-form :model="taskSettings" label-width="120px">
            <el-form-item label="最大并发任务">
              <el-input-number v-model="taskSettings.max_concurrent_tasks" :min="1" :max="100" />
              <span class="form-hint">同时执行的最大任务数</span>
            </el-form-item>
            <el-form-item label="任务超时(秒)">
              <el-input-number v-model="taskSettings.task_timeout" :min="30" :max="3600" />
              <span class="form-hint">任务执行超时时间</span>
            </el-form-item>
            <el-form-item label="最大重试次数">
              <el-input-number v-model="taskSettings.max_retries" :min="0" :max="10" />
              <span class="form-hint">任务失败后的重试次数</span>
            </el-form-item>
            <el-form-item label="重试间隔(秒)">
              <el-input-number v-model="taskSettings.retry_interval" :min="1" :max="300" />
              <span class="form-hint">重试之间的等待时间</span>
            </el-form-item>
            <el-form-item label="队列最大长度">
              <el-input-number v-model="taskSettings.max_queue_size" :min="10" :max="10000" />
              <span class="form-hint">任务队列最大容量</span>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 代理设置 -->
      <el-tab-pane label="代理设置" name="agents">
        <el-card>
          <template #header>
            <span>代理配置</span>
          </template>
          <el-form :model="agentSettings" label-width="120px">
            <el-form-item label="最大代理数">
              <el-input-number v-model="agentSettings.max_agents" :min="1" :max="50" />
              <span class="form-hint">系统支持的最大代理数量</span>
            </el-form-item>
            <el-form-item label="代理超时(秒)">
              <el-input-number v-model="agentSettings.agent_timeout" :min="30" :max="600" />
              <span class="form-hint">代理执行超时时间</span>
            </el-form-item>
            <el-form-item label="心跳间隔(秒)">
              <el-input-number v-model="agentSettings.heartbeat_interval" :min="5" :max="60" />
              <span class="form-hint">代理心跳检测间隔</span>
            </el-form-item>
            <el-form-item label="心跳超时(秒)">
              <el-input-number v-model="agentSettings.heartbeat_timeout" :min="30" :max="300" />
              <span class="form-hint">代理心跳超时时间</span>
            </el-form-item>
            <el-form-item label="自动重启">
              <el-switch v-model="agentSettings.auto_restart" />
              <span class="form-hint">代理崩溃后自动重启</span>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 模型设置 -->
      <el-tab-pane label="模型设置" name="models">
        <el-card>
          <template #header>
            <span>模型配置</span>
          </template>
          <el-form :model="modelSettings" label-width="120px">
            <el-form-item label="默认模型">
              <el-select v-model="modelSettings.default_model">
                <el-option label="GPT-4" value="gpt-4" />
                <el-option label="GPT-3.5 Turbo" value="gpt-3.5-turbo" />
                <el-option label="Claude 3 Opus" value="claude-3-opus" />
                <el-option label="Claude 3 Sonnet" value="claude-3-sonnet" />
              </el-select>
              <span class="form-hint">未指定模型时使用的默认模型</span>
            </el-form-item>
            <el-form-item label="最大Token">
              <el-input-number v-model="modelSettings.max_tokens" :min="256" :max="128000" />
              <span class="form-hint">单次请求的最大Token数</span>
            </el-form-item>
            <el-form-item label="温度">
              <el-slider v-model="modelSettings.temperature" :min="0" :max="2" :step="0.1" show-input />
              <span class="form-hint">生成文本的随机性（0=确定，2=随机）</span>
            </el-form-item>
            <el-form-item label="速率限制">
              <el-input-number v-model="modelSettings.rate_limit" :min="1" :max="1000" />
              <span class="form-hint">每分钟最大请求数</span>
            </el-form-item>
            <el-form-item label="成本限制($)">
              <el-input-number v-model="modelSettings.cost_limit" :min="0" :max="1000" :precision="2" />
              <span class="form-hint">每日最大API成本</span>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 缓存设置 -->
      <el-tab-pane label="缓存设置" name="cache">
        <el-card>
          <template #header>
            <span>缓存配置</span>
          </template>
          <el-form :model="cacheSettings" label-width="120px">
            <el-form-item label="启用缓存">
              <el-switch v-model="cacheSettings.enabled" />
              <span class="form-hint">启用结果缓存以提高性能</span>
            </el-form-item>
            <el-form-item label="缓存类型">
              <el-select v-model="cacheSettings.type">
                <el-option label="内存缓存" value="memory" />
                <el-option label="Redis缓存" value="redis" />
              </el-select>
            </el-form-item>
            <el-form-item label="缓存大小">
              <el-input-number v-model="cacheSettings.max_size" :min="100" :max="100000" />
              <span class="form-hint">最大缓存条目数</span>
            </el-form-item>
            <el-form-item label="缓存TTL(秒)">
              <el-input-number v-model="cacheSettings.ttl" :min="60" :max="86400" />
              <span class="form-hint">缓存过期时间</span>
            </el-form-item>
            <el-form-item>
              <el-button type="danger" @click="clearCache">
                <el-icon><Delete /></el-icon>
                清除缓存
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 安全设置 -->
      <el-tab-pane label="安全设置" name="security">
        <el-card>
          <template #header>
            <span>安全配置</span>
          </template>
          <el-form :model="securitySettings" label-width="120px">
            <el-form-item label="启用认证">
              <el-switch v-model="securitySettings.auth_enabled" />
              <span class="form-hint">启用API认证</span>
            </el-form-item>
            <el-form-item label="API密钥">
              <el-input v-model="securitySettings.api_key" type="password" show-password />
              <span class="form-hint">API访问密钥</span>
            </el-form-item>
            <el-form-item label="JWT密钥">
              <el-input v-model="securitySettings.jwt_secret" type="password" show-password />
              <span class="form-hint">JWT令牌密钥</span>
            </el-form-item>
            <el-form-item label="Token过期(秒)">
              <el-input-number v-model="securitySettings.token_expiry" :min="300" :max="86400" />
              <span class="form-hint">JWT令牌过期时间</span>
            </el-form-item>
            <el-form-item label="启用CORS">
              <el-switch v-model="securitySettings.cors_enabled" />
              <span class="form-hint">启用跨域资源共享</span>
            </el-form-item>
            <el-form-item label="允许来源">
              <el-input v-model="securitySettings.cors_origins" placeholder="http://localhost:3000" />
              <span class="form-hint">允许的跨域来源（逗号分隔）</span>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 通知设置 -->
      <el-tab-pane label="通知设置" name="notifications">
        <el-card>
          <template #header>
            <span>通知配置</span>
          </template>
          <el-form :model="notificationSettings" label-width="120px">
            <el-form-item label="启用通知">
              <el-switch v-model="notificationSettings.enabled" />
              <span class="form-hint">启用系统通知</span>
            </el-form-item>
            <el-form-item label="邮件通知">
              <el-switch v-model="notificationSettings.email_enabled" />
              <span class="form-hint">启用邮件通知</span>
            </el-form-item>
            <el-form-item label="SMTP服务器">
              <el-input v-model="notificationSettings.smtp_host" placeholder="smtp.gmail.com" />
            </el-form-item>
            <el-form-item label="SMTP端口">
              <el-input-number v-model="notificationSettings.smtp_port" :min="25" :max="65535" />
            </el-form-item>
            <el-form-item label="发件人邮箱">
              <el-input v-model="notificationSettings.smtp_from" placeholder="noreply@example.com" />
            </el-form-item>
            <el-form-item label="Webhook URL">
              <el-input v-model="notificationSettings.webhook_url" placeholder="https://hooks.slack.com/..." />
              <span class="form-hint">Slack/钉钉/企业微信 Webhook</span>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 存储设置 -->
      <el-tab-pane label="存储设置" name="storage">
        <el-card>
          <template #header>
            <span>存储配置</span>
          </template>
          <el-form :model="storageSettings" label-width="120px">
            <el-form-item label="数据目录">
              <el-input v-model="storageSettings.data_dir" placeholder="./data" />
              <span class="form-hint">数据存储目录</span>
            </el-form-item>
            <el-form-item label="日志目录">
              <el-input v-model="storageSettings.log_dir" placeholder="./logs" />
              <span class="form-hint">日志存储目录</span>
            </el-form-item>
            <el-form-item label="备份目录">
              <el-input v-model="storageSettings.backup_dir" placeholder="./backups" />
              <span class="form-hint">备份存储目录</span>
            </el-form-item>
            <el-form-item label="自动备份">
              <el-switch v-model="storageSettings.auto_backup" />
              <span class="form-hint">启用自动备份</span>
            </el-form-item>
            <el-form-item label="备份间隔(小时)">
              <el-input-number v-model="storageSettings.backup_interval" :min="1" :max="168" />
              <span class="form-hint">自动备份间隔</span>
            </el-form-item>
            <el-form-item label="保留天数">
              <el-input-number v-model="storageSettings.backup_retention" :min="1" :max="365" />
              <span class="form-hint">备份保留天数</span>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Check, Delete } from '@element-plus/icons-vue'

const activeTab = ref('basic')

// 基本设置
const basicSettings = ref({
  app_name: 'AI多代理系统',
  app_description: '一个稳定、可自定义的AI多代理系统',
  log_level: 'INFO',
  language: 'zh-CN',
  timezone: 'Asia/Shanghai'
})

// 任务设置
const taskSettings = ref({
  max_concurrent_tasks: 5,
  task_timeout: 300,
  max_retries: 3,
  retry_interval: 60,
  max_queue_size: 1000
})

// 代理设置
const agentSettings = ref({
  max_agents: 10,
  agent_timeout: 120,
  heartbeat_interval: 10,
  heartbeat_timeout: 120,
  auto_restart: true
})

// 模型设置
const modelSettings = ref({
  default_model: 'gpt-4',
  max_tokens: 4096,
  temperature: 0.7,
  rate_limit: 60,
  cost_limit: 100
})

// 缓存设置
const cacheSettings = ref({
  enabled: true,
  type: 'memory',
  max_size: 1000,
  ttl: 3600
})

// 安全设置
const securitySettings = ref({
  auth_enabled: false,
  api_key: '',
  jwt_secret: '',
  token_expiry: 3600,
  cors_enabled: true,
  cors_origins: 'http://localhost:3000'
})

// 通知设置
const notificationSettings = ref({
  enabled: false,
  email_enabled: false,
  smtp_host: '',
  smtp_port: 587,
  smtp_from: '',
  webhook_url: ''
})

// 存储设置
const storageSettings = ref({
  data_dir: './data',
  log_dir: './logs',
  backup_dir: './backups',
  auto_backup: true,
  backup_interval: 24,
  backup_retention: 30
})

function saveSettings() {
  ElMessage.success('设置已保存')
}

function clearCache() {
  ElMessage.success('缓存已清除')
}
</script>

<style scoped>
.settings-container {
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.form-hint {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-card) {
  margin-bottom: 16px;
}
</style>
