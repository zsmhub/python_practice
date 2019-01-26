-- 此项目对应数据库所需表SQL

CREATE TABLE `tenxun_android` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `company` varchar(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `appid` char(15) NOT NULL DEFAULT '' COMMENT 'appid',
  `app_alias` varchar(32) NOT NULL DEFAULT '' COMMENT '应用名称',
  `add_time` char(10) NOT NULL DEFAULT '' COMMENT '添加日期',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique` (`appid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='腾讯开放平台各公司对应的安卓应用';

CREATE TABLE `tenxun_cbs` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `company` varchar(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `app_alias` varchar(32) NOT NULL DEFAULT '' COMMENT '应用名称',
  `month` char(10) NOT NULL DEFAULT '' COMMENT '结算月份',
  `number` varchar(100) NOT NULL DEFAULT '' COMMENT '结算单号',
  `init_income` decimal(20,2) NOT NULL COMMENT '原始收入（元）',
  `settle_income` decimal(20,2) NOT NULL COMMENT '结算收入（元）',
  `service_fee` decimal(20,2) NOT NULL COMMENT '服务费（元）',
  `settle_status` char(10) NOT NULL DEFAULT '' COMMENT '结算状态',
  `add_time` char(10) NOT NULL DEFAULT '' COMMENT '添加日期',
  `is_del` char(10) NOT NULL DEFAULT '' COMMENT '是否删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique` (`number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='腾讯开放平台结算数据';

CREATE TABLE `tenxun_yyb` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `company` varchar(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `app_alias` varchar(32) NOT NULL DEFAULT '' COMMENT '应用名称',
  `date` char(10) NOT NULL DEFAULT '' COMMENT '日期',
  `amount` decimal(20,2) NOT NULL DEFAULT '0.00' COMMENT '金额',
  `add_time` char(19) NOT NULL DEFAULT '' COMMENT '添加时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique` (`company`,`app_alias`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='腾讯开放平台对账数据';
