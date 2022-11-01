{{/*
    Expand the name of the chart.
*/}}
{{- define "common.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
    Create a default fully qualified app name.
    We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
    If release name contains chart name it will be used as a full name.
*/}}
{{- define "common.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
    Create chart name and version as used by the chart label.
*/}}
{{- define "common.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
    Common labels for all resources.
*/}}
{{- define "common.labels" -}}
helm.sh/chart: {{ include "common.chart" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{ with .Values.common.labels }}
{{- toYaml . }}
{{- end }}
{{- end }}

{{/*
    Create the name of the service account to use.
*/}}
{{- define "common.serviceAccount.name" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "common.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
    Assemble partial image specs into name.
*/}}
{{- define "app.image" -}}
{{- printf "%s:%s" .Values.app.image.repository (default .Chart.AppVersion .Values.app.image.tag) }}
{{- end }}

{{/*
    Create application secret key if not specified.
    If secret exists (when upgrading), reuse it.
*/}}
{{- define "app.config.secretKey" -}}
{{- if $existingSecret := (lookup "v1" "Secret" .Release.Namespace (include "common.fullname" .)) }}
{{- b64dec $existingSecret.data.DJANGO_SECRET_KEY }}
{{- else }}
{{- default (randAlphaNum 32) .Values.app.config.secretKey }}
{{- end }}
{{- end }}

{{/*
    Database URL for application.
    By default, configured to use `postgresql` subchart.
*/}}
{{- define "app.config.databaseURL" -}}
{{- if .Values.app.config.databaseURL }}
{{- tpl .Values.app.config.databaseURL $ }}
{{- else }}
{{- if .Values.postgresql.enabled }}
{{- printf "postgres://postgres:password@%s:5432/postgres" (include "postgresql.primary.fullname" .Subcharts.postgresql) }}
{{- end }}
{{- end }}
{{- end }}

{{/*
    Remote cache URL for application.
    By default, configured to use `redis` subchart.
*/}}
{{- define "app.config.cacheURL" -}}
{{- if .Values.app.config.cacheURL }}
{{- tpl .Values.app.config.cacheURL $ }}
{{- else }}
{{- if .Values.redis.enabled }}
{{- printf "redis://%s-master:6379" (include "common.names.fullname" .Subcharts.redis) }}
{{- end }}
{{- end }}
{{- end }}

{{/*
    Message broker URL for application.
    By default, configured to use `rabbitmq` subchart.
*/}}
{{- define "app.config.messageBrokerURL" -}}
{{- if .Values.app.config.messageBrokerURL }}
{{- tpl .Values.app.config.messageBrokerURL $ }}
{{- else }}
{{- if .Values.rabbitmq.enabled }}
{{- printf "amqp://user:password@%s:5672/" (include "common.names.fullname" .Subcharts.rabbitmq) }}
{{- end }}
{{- end }}
{{- end }}

{{/*
    Application core server component full name.
*/}}
{{- define "app.components.server.fullname" -}}
{{- printf "%s-server" (include "common.fullname" .) }}
{{- end }}

{{/*
    Application core server component labels.
*/}}
{{- define "app.components.server.labels" -}}
{{ include "common.labels" . }}
app.kubernetes.io/component: server
{{ include "app.components.server.selectorLabels" . }}
{{- end }}

{{/*
    Application core server component labels.
*/}}
{{- define "app.components.server.selectorLabels" -}}
app.kubernetes.io/name: "{{ include "common.name" . }}-server"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
    Application worker component full name.
*/}}
{{- define "app.components.worker.fullname" -}}
{{- printf "%s-worker" (include "common.fullname" .) }}
{{- end }}

{{/*
    Application worker component labels.
*/}}
{{- define "app.components.worker.labels" -}}
{{ include "common.labels" . }}
app.kubernetes.io/component: worker
{{ include "app.components.worker.selectorLabels" . }}
{{- end }}

{{/*
    Application worker component labels.
*/}}
{{- define "app.components.worker.selectorLabels" -}}
app.kubernetes.io/name: "{{ include "common.name" . }}-worker"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
    Application periodic scheduler component full name.
*/}}
{{- define "app.components.periodicScheduler.fullname" -}}
{{- printf "%s-periodic-scheduler" (include "common.fullname" .) }}
{{- end }}

{{/*
    Application periodic scheduler component labels.
*/}}
{{- define "app.components.periodicScheduler.labels" -}}
{{ include "common.labels" . }}
app.kubernetes.io/component: periodic-scheduler
{{ include "app.components.periodicScheduler.selectorLabels" . }}
{{- end }}

{{/*
    Application periodic scheduler component labels.
*/}}
{{- define "app.components.periodicScheduler.selectorLabels" -}}
app.kubernetes.io/name: "{{ include "common.name" . }}-periodic-scheduler"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
