import Main from '@/view/main'
import Login from '@/view/login'
import ConfigKibana from '@/view/system-config/config-kibana.vue'
import ConfigElasticsearch from '@/view/system-config/config-elasticsearch.vue'
import ConfigLogstash from '@/view/system-config/config-logstash.vue'
import ConfigFilebeat from '@/view/system-config/config-filebeat.vue'
import ConfigAPM from '@/view/system-config/config-apm.vue'
import ConfigKafka from '@/view/system-config/config-kafka.vue'
import ConfigZookeeper from '@/view/system-config/config-zookeeper.vue'
import DeployFilebeat from '@/view/deploy-software/deploy-filebeat.vue'
import DeployAPMServer from '@/view/deploy-software/deploy-apmserver.vue'
import DeployAPMJavaClient from '@/view/deploy-software/deploy-apmjavaclient.vue'
import KafkaOperator from '@/view/system-operation/operation-kafka.vue'

import Operation from '@/view/components/operation'
import parentView from '@/components/parent-view'

/**
 * iview-admin中meta除了原生参数外可配置的参数:
 * meta: {
 *  hideInMenu: (false) 设为true后在左侧菜单不会显示该页面选项
 *  notCache: (false) 设为true后页面不会缓存
 *  access: (null) 可访问该页面的权限数组，当前路由设置的权限会影响子路由
 *  icon: (-) 该页面在左侧菜单、面包屑和标签导航处显示的图标，如果是自定义图标，需要在图标名称前加下划线'_'
 * }
 */

const OverView = {template: '<div><h1>Welcome!</h1><p>Here is what site is about.</p></div>'}

export default [
  {
    path: '/login',
    name: 'login',
    meta: {
      title: 'Login - 登录',
      hideInMenu: true
    },
    component: Login
  },
  {
    path: '/',
    name: '_home',
    redirect: 'home',
    component: Main,
    meta: {
      hideInMenu: true,
      notCache: true
    }
    ,
    children: [
      {
        path: '/home',
        name: 'home',
        meta: {
          hideInMenu: true,
          title: '首页',
          notCache: true
        },
        component: ConfigElasticsearch
      },
    ]
  }
  ,
  {
    path: '/elasticsearch',
    name: 'Elasticsearch',
    meta: {
      icon: "md-construct",
      title: 'Elasticsearch'
    }
    ,
    component: Main,
    children: [
      {
        path: '/elasticsearch/deploy',
        name: 'ES集群部署',
        meta: {
          icon: 'md-menu',
          title: 'ES集群部署'
        },
        component: ConfigElasticsearch
      },
      {
        path: '/elasticsearch/configuration',
        name: 'ES配置更新',
        meta: {
          icon: 'md-menu',
          title: 'ES配置更新'
        },
        component: ConfigElasticsearch
      },
      {
        path: '/elasticsearch/operation',
        name: 'ES服务管理',
        meta: {
          icon: 'md-menu',
          title: 'ES服务管理'
        },
        component: ConfigElasticsearch
      },
      {
        path: '/elasticsearch/plugins',
        name: 'ES插件管理',
        meta: {
          icon: 'md-menu',
          title: 'ES插件管理'
        },
        component: ConfigElasticsearch
      }
    ]
  },
  {
    path: '/logstash',
    name: 'Logstash',
    meta: {
      icon: "md-construct",
      title: 'Logstash'
    }
    ,
    component: Main,
    children: [
      {
        path: '/logstash/deploy',
        name: 'Logstash部署',
        meta: {
          icon: 'md-menu',
          title: 'Logstash部署'
        },
        component: ConfigLogstash
      },
      {
        path: '/logstash/configuration',
        name: 'Logstash配置更新',
        meta: {
          icon: 'md-menu',
          title: 'Logstash配置更新'
        },
        component: ConfigLogstash
      },
      {
        path: '/logstash/operation',
        name: 'Logstash服务管理',
        meta: {
          icon: 'md-menu',
          title: 'Logstash服务管理'
        },
        component: ConfigElasticsearch
      },
      {
        path: '/logstash/plugins',
        name: 'Logstash插件管理',
        meta: {
          icon: 'md-menu',
          title: 'logstash插件管理'
        },
        component: ConfigElasticsearch
      }
    ]
  },
  {
    path: '/kibana',
    name: 'Kibana',
    meta: {
      icon: "md-construct",
      title: 'Kibana'
    }
    ,
    component: Main,
    children: [
      {
        path: '/kibana/deploy',
        name: 'Kibana部署',
        meta: {
          icon: 'md-menu',
          title: 'Kibana部署'
        },
        component: ConfigKibana
      },
      {
        path: '/kibana/configuration',
        name: 'Kibana配置更新',
        meta: {
          icon: 'md-menu',
          title: 'Kibana配置更新'
        },
        component: ConfigKibana
      },
      {
        path: '/kibana/operation',
        name: 'Kibana服务管理',
        meta: {
          icon: 'md-menu',
          title: 'Kibana服务管理'
        },
        component: ConfigElasticsearch
      },
      {
        path: '/kibana/plugins',
        name: 'Kibana插件管理',
        meta: {
          icon: 'md-menu',
          title: 'Kibana插件管理'
        },
        component: ConfigElasticsearch
      }
    ]
  },
  {
    path: '/apm',
    name: 'APM',
    meta: {
      icon: "md-construct",
      title: 'APM'
    }
    ,
    component: Main,
    children: [
      {
        path: '/apm/deploy',
        name: 'APM Server部署',
        meta: {
          icon: 'md-menu',
          title: 'APM Server部署'
        },
        component: DeployAPMServer
      },
      {
        path: '/apm/configuration',
        name: 'APM Server配置更新',
        meta: {
          icon: 'md-menu',
          title: 'APM Server配置更新'
        },
        component: ConfigAPM
      },
      {
        path: '/apm/client/deploy',
        name: 'APM Java Agent部署',
        meta: {
          icon: 'md-menu',
          title: 'APM Java Agent部署'
        },
        component: DeployAPMJavaClient
      },
      {
        path: '/apm/client',
        name: 'APM Java Agent配置更新',
        meta: {
          icon: 'md-menu',
          title: 'APM Java Agent配置更新'
        },
        component: ConfigAPM
      }
    ]
  },
  {
    path: '/beats',
    name: 'BEATS',
    meta: {
      icon: "md-construct",
      title: 'BEATS'
    }
    ,
    component: Main,
    children: [
      {
        path: '/beats/filebeat-deploy',
        name: 'Filebeat客户端部署',
        meta: {
          icon: 'md-menu',
          title: 'Filebeat客户端部署'
        },
        component: DeployFilebeat
      },
      {
        path: '/beats/filebeat-configuration',
        name: 'Filebeat配置更新',
        meta: {
          icon: 'md-menu',
          title: 'Filebeat配置更新'
        },
        component: ConfigFilebeat
      }
    ]
  },
  {
    path: '/curator',
    name: 'curator',
    meta: {
      icon: "md-construct",
      title: 'Curator'
    }
    ,
    component: Main,
    children: [
      {
        path: '/curator/deploy',
        name: 'curator部署',
        meta: {
          icon: 'md-menu',
          title: 'curator部署'
        },
        component: ConfigKibana
      },
      {
        path: '/curator/configuration',
        name: 'curator配置更新',
        meta: {
          icon: 'md-menu',
          title: 'curator配置更新'
        },
        component: ConfigKafka
      }
    ]
  },
  {
    path: '/kafka',
    name: 'kafka',
    meta: {
      icon: "md-construct",
      title: 'Kafka'
    }
    ,
    component: Main,
    children: [
      {
        path: '/kafka/deploy',
        name: 'kafka部署',
        meta: {
          icon: 'md-menu',
          title: 'kafka部署'
        },
        component: ConfigKibana
      },
      {
        path: '/kafka/configuration',
        name: 'kafka配置更新',
        meta: {
          icon: 'md-menu',
          title: 'kafka配置更新'
        },
        component: ConfigKafka
      },
      {
        path: '/kafka/operation',
        name: 'kafka服务管理',
        meta: {
          icon: 'md-menu',
          title: 'kafka服务管理'
        },
        component: KafkaOperator
      }
    ]
  }
  ,
  {
    path: '/zookeeper',
    name: 'zookeeper',
    meta: {
      icon: "md-construct",
      title: 'Zookeeper'
    }
    ,
    component: Main,
    children: [
      {
        path: '/zookeeper/deploy',
        name: 'zookeeper部署',
        meta: {
          icon: 'md-menu',
          title: 'zookeeper部署'
        },
        component: ConfigZookeeper
      },
      {
        path: '/zookeeper/configuration',
        name: 'zookeeper配置更新',
        meta: {
          icon: 'md-menu',
          title: 'zookeeper配置更新'
        },
        component: ConfigZookeeper
      }
    ]
  }
  ,
  {
    path: '/overview',
    name: 'overview',
    component: OverView
  },
  {
    path: '/401',
    name: 'error_401',
    component: () =>
    import
      ('@/view/error-page/401.vue'
)
}
,
{
  path: '/500',
    name
:
  'error_500',
    component
:
  () =>
import
  ('@/view/error-page/500.vue')
}
,
{
  path: '*',
    name
:
  'error_404',
    component
:
  () =>
import
  ('@/view/error-page/404.vue')
}
]
