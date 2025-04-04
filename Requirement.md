https://platform.amfori.org/ui/monitoring/monitoring-partner-planning/ongoing 
写python程序，爬取这一页的内容，需求如下：
1. 抓取to confirm的列表，将列表中的内容抓取下来，同时也将每一行的链接取出来。保存到一个Excel表格中。
2. 要求程序每次执行时，如果有新增就添加，如果有更新就更新内容，以'Site amfori ID'不主键判断是新增还是更新。
3. 如果有多页，就翻页抓取下一页的内容，直至全部抓取完成。
4. 在每个行中增加三列列，一列为新增创建时间，一列为更新时间（每次更新后，保存更新时间）,最后一列为抓取时间
5. 请将Scraped At放到一第列。
6. 增加一个需求：在第一列前增加一列‘状态’，如果当前excel中的记录，在当前抓取的列表中没有了，表示该记录已经的执行确认过了，需要将该行记录标记为“已确认”，如是本次新增的，状态标记为‘新增’，如果是更新过的，请标记为‘更新记录’


 - 流程：
1. 用selenium之类的工作模拟用户登陆，登陆页面URL： https://sso.amfori.org/auth/realms/amfori/protocol/openid-connect/auth?client_id=sustainability-platform&response_type=code&scope=openid&redirect_uri=https%3A%2F%2Fplatform.amfori.org%2Fui%2Fmonitoring%2Fmonitoring-partner-planning%2Fongoing&state=a28d7a40-cd22-4662-9c76-03d7ec5a52dd&nonce=dc68a6eb-8948-43d2-822c-2be129ae83e6

2. 然后定向到页面https://platform.amfori.org/ui/monitoring/monitoring-partner-planning/ongoing，查询条件：
   在To Confirm区域如下查询：
country: China
initiative: BSCI 和 QMI

3. 点击filer按钮后会调用：https://platform.amfori.org/v1/services/monitoring/monitoring-partner-plannings/to-confirm/search?childQuery=&parentQuery=%2B(+monitoredSite.address.country.en_GB:China+)+%2B(+monitoringInitiative.en_GB:BSCI+QMI)&rows=25&sort=&sortOrder=&start=0

我们需要先通过用户名和密码登录，然后获取 token，最后使用 token 访问 API。

1. 取得的response如下：
--------------Response start----------------
{
  "results" : [ {
    "monitoredSite" : {
      "name" : "Mao Fa Toys And Gift Corporation Ltd",
      "localName" : "泉州市茂发玩具礼品有限公司(913505217531209207)",
      "address" : {
        "street" : "No.1571 Yucheng Village, Zhangban Town, Taiwanese Investment District",
        "zip" : "362100",
        "city" : "Quanzhou",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "Quanzhou Junyang trade IMP. & EXP. CO LTD.",
      "managedByBusinessPartnerAmforiId" : "156-035945-000",
      "siteAmforiId" : "156-035945-002",
      "externalReference" : "BSCI_dbid_368410"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1746921600000,
    "beingReplanned" : false,
    "uuid" : "57a05cff-9cfc-4273-91a8-5198c6c6810a",
    "timeWindowFrom" : 1744329600000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "24-0250779-1",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FOLLOW_UP_MONITORING",
      "en_GB" : "Follow-up Monitoring",
      "tr_TR" : "Takip Denetimi",
      "zh_CN" : "跟进监测"
    },
    "requestorLegalName" : "El Corte Inglés,S.A",
    "requestDate" : 1743139830039,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743139830058
    },
    "esLastIndexedTimestamp" : 1743139830133
  }, {
    "monitoredSite" : {
      "name" : "YIWU SAIQIAO JEWELRY CO., LTD",
      "localName" : "义乌赛巧饰品有限公司(91330782MA2DB8R14C)",
      "address" : {
        "street" : "5F, Building 6, 777 Chouyi East Road, Choujiang Street, Yiwu City, Zhejiang Province",
        "zip" : "322000",
        "city" : "YIWU",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "YIWU SAIQIAO JEWELRY CO.,LTD",
      "managedByBusinessPartnerAmforiId" : "156-013915-000",
      "siteAmforiId" : "156-013915-003"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1746921600000,
    "beingReplanned" : false,
    "uuid" : "6eca888c-4d0f-4f7c-855b-9c5e6efae88d",
    "timeWindowFrom" : 1744329600000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "24-0250231-1",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FOLLOW_UP_MONITORING",
      "en_GB" : "Follow-up Monitoring",
      "tr_TR" : "Takip Denetimi",
      "zh_CN" : "跟进监测"
    },
    "requestorLegalName" : "Avec BV",
    "requestDate" : 1743145206119,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743145206138
    },
    "esLastIndexedTimestamp" : 1743145206227
  }, {
    "monitoredSite" : {
      "name" : "Jiangxi Jiayinking Culture Technology Company Limited.",
      "address" : {
        "street" : "Block K3-17, Electronic Information Industry Science and Technology City, Longnan Economic and Technological Development Zone, Longnan City,",
        "city" : "Ganzhou",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "Jiangxi Jiayinking Culture Technology Company Limited",
      "managedByBusinessPartnerAmforiId" : "156-035418-000",
      "siteAmforiId" : "156-035418-002"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1746748800000,
    "beingReplanned" : false,
    "uuid" : "e1abe644-7762-44f3-b89c-1317a73c93f8",
    "timeWindowFrom" : 1744329600000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "25-0319176",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FULL_MONITORING",
      "en_GB" : "Full Monitoring",
      "tr_TR" : "Tam Denetim",
      "zh_CN" : "全面监测活动"
    },
    "requestorLegalName" : "EVERGREAT CHINA LIMITED",
    "requestDate" : 1743137442742,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743137442760
    },
    "esLastIndexedTimestamp" : 1743137442867
  }, {
    "monitoredSite" : {
      "name" : "Huidong Hua Xin Industrial Co., Ltd.",
      "localName" : "惠东县华鑫实业有限公司",
      "address" : {
        "street" : "No.12, 3Xiang, Xiamahu Road, Huangpai, Pingshan Town, Huidong County",
        "city" : "huizhou",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "Huidong Hua Xin Industrial Co., Ltd.",
      "managedByBusinessPartnerAmforiId" : "156-035405-000",
      "siteAmforiId" : "156-035405-001"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1746748800000,
    "beingReplanned" : false,
    "uuid" : "078de932-8616-4704-81a6-826b7bc60088",
    "timeWindowFrom" : 1744329600000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "24-0250854-1",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FOLLOW_UP_MONITORING",
      "en_GB" : "Follow-up Monitoring",
      "tr_TR" : "Takip Denetimi",
      "zh_CN" : "跟进监测"
    },
    "requestorLegalName" : "Amazon.com, Inc.",
    "requestDate" : 1743145715014,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743145715061
    },
    "esLastIndexedTimestamp" : 1743145715355
  }, {
    "monitoredSite" : {
      "name" : "Pujiang Chiyuan Industry and Trade Co., Ltd",
      "localName" : "浦江驰源工贸有限公司(913307267864230557)",
      "address" : {
        "street" : "No. 55 Yidianhong Avenue, Pujiang County",
        "zip" : "322200",
        "city" : "Jinhua",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "Pujiang Chiyuan Industry and Trade Co., Ltd",
      "managedByBusinessPartnerAmforiId" : "156-034524-000",
      "siteAmforiId" : "156-034524-001"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1746835200000,
    "beingReplanned" : false,
    "uuid" : "4519691b-8f37-416d-b04f-ac9026266cba",
    "timeWindowFrom" : 1744329600000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "25-0319223",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FULL_MONITORING",
      "en_GB" : "Full Monitoring",
      "tr_TR" : "Tam Denetim",
      "zh_CN" : "全面监测活动"
    },
    "requestorLegalName" : "NINGBO FREE WILL IMP&EXP CO.,LTD",
    "requestDate" : 1743146903354,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743146903368
    },
    "esLastIndexedTimestamp" : 1743146903433
  }, {
    "monitoredSite" : {
      "name" : "Yunhe Fenglin crafts Co., LTD",
      "address" : {
        "street" : "No. 4, Jiefang West Street,  Fenghuangshan Subdistrict ,Yunhe County,Lishui City, Zhejiang Province",
        "city" : "Lishui",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "Yunhe Fenglin crafts Co., LTD",
      "managedByBusinessPartnerAmforiId" : "156-062091-000",
      "siteAmforiId" : "156-062091-001"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1746748800000,
    "beingReplanned" : false,
    "uuid" : "2a9a6baf-3416-49c4-afa5-31ccaa84f491",
    "timeWindowFrom" : 1744329600000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "25-0319161",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FULL_MONITORING",
      "en_GB" : "Full Monitoring",
      "tr_TR" : "Tam Denetim",
      "zh_CN" : "全面监测活动"
    },
    "requestorLegalName" : "MWH GmbH",
    "requestDate" : 1743131167826,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743131167839
    },
    "esLastIndexedTimestamp" : 1743131167919
  }, {
    "monitoredSite" : {
      "name" : "THE FIRST BRANCH OF FOSHAN CITY SHUNDE DISTRICT JIAHE INDUSTRIAL CO., LTD",
      "localName" : "佛山市顺德区嘉和实业有限公司第一分公司",
      "address" : {
        "street" : "4/F A1 No. 2 Shizhou, Baichen Rd, Gangbei Industrial Park, Shizhou Village, Chencun, Shunde ",
        "city" : "Foshan",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "THE FIRST BRANCH OF FOSHAN CITY SHUNDE DISTRICT JIAHE INDUSTRIAL CO., LTD",
      "managedByBusinessPartnerAmforiId" : "156-037154-000",
      "siteAmforiId" : "156-037154-001"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1746835200000,
    "beingReplanned" : false,
    "uuid" : "e564c2f3-fe68-44de-8359-b5b6e686bafc",
    "timeWindowFrom" : 1744329600000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "25-0319170",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FULL_MONITORING",
      "en_GB" : "Full Monitoring",
      "tr_TR" : "Tam Denetim",
      "zh_CN" : "全面监测活动"
    },
    "requestorLegalName" : "J-Trade Handels AB",
    "requestDate" : 1743134406775,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743134406800
    },
    "esLastIndexedTimestamp" : 1743134406961
  }, {
    "monitoredSite" : {
      "name" : "Guilin Bamboo Forever Technology Co., Ltd",
      "localName" : "桂林一生竹科技有限责任公司",
      "address" : {
        "street" : "Building 1#, No.4, Chengxiang Road, Lingchuan Town, Lingchuan County",
        "city" : "Guilin",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "Guilin Bamboo Forever Technology Co., Ltd.",
      "managedByBusinessPartnerAmforiId" : "156-040102-000",
      "siteAmforiId" : "156-040102-002"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1746748800000,
    "beingReplanned" : false,
    "uuid" : "69b65ab0-f2df-44a5-97f7-cadaa2b05dab",
    "timeWindowFrom" : 1744329600000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "24-0273488-1",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FOLLOW_UP_MONITORING",
      "en_GB" : "Follow-up Monitoring",
      "tr_TR" : "Takip Denetimi",
      "zh_CN" : "跟进监测"
    },
    "requestorLegalName" : "EVERGREAT CHINA LIMITED",
    "requestDate" : 1743143365070,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743143365088
    },
    "esLastIndexedTimestamp" : 1743143365157
  }, {
    "monitoredSite" : {
      "name" : "Yangzhou Aolikes Sports Goods Co., Ltd.",
      "localName" : "扬州奥力克斯体育用品有限公司（91321012687803239D）",
      "address" : {
        "street" : "No.8, Fumin Road, Fumin Industrial Zone, Xiaoji Town, Jiangdu District",
        "city" : "Yangzhou City",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "Yangzhou Aolikes Sports Goods Co., Ltd.",
      "managedByBusinessPartnerAmforiId" : "156-045953-000",
      "siteAmforiId" : "156-045953-001"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1746748800000,
    "beingReplanned" : false,
    "uuid" : "e09993d6-f37f-48d0-889b-97fbcf4f138c",
    "timeWindowFrom" : 1744329600000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "25-0319229",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FULL_MONITORING",
      "en_GB" : "Full Monitoring",
      "tr_TR" : "Tam Denetim",
      "zh_CN" : "全面监测活动"
    },
    "requestorLegalName" : "D & F Commodity Trade B.V.",
    "requestDate" : 1743148001204,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743148001222
    },
    "esLastIndexedTimestamp" : 1743148001296
  }, {
    "monitoredSite" : {
      "name" : "Ninghai Nade Commodity Limited Company",
      "localName" : "宁海县纳德日用品有限公司(91330226MA283RXT53)",
      "address" : {
        "street" : "Building 3, No.626, Wangjia Village, Xidian Town, Ninghai County",
        "zip" : "315600",
        "city" : "Ningbo",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "Ninghai Nade Commodity Limited Company",
      "managedByBusinessPartnerAmforiId" : "156-024484-000",
      "siteAmforiId" : "156-024484-002"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1746835200000,
    "beingReplanned" : false,
    "uuid" : "5a460093-2228-4a02-8428-5fa179164c6d",
    "timeWindowFrom" : 1744416000000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "25-0319234",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FULL_MONITORING",
      "en_GB" : "Full Monitoring",
      "tr_TR" : "Tam Denetim",
      "zh_CN" : "全面监测活动"
    },
    "requestorLegalName" : "The Cookware Company Europe BV",
    "requestDate" : 1743149940002,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743149940023
    },
    "esLastIndexedTimestamp" : 1743149940118
  }, {
    "monitoredSite" : {
      "name" : "Dongguan Chuangtong Shiji Technology Co.,Ltd",
      "localName" : "东莞创通视际科技有限公司",
      "address" : {
        "street" : "&Room 801,\nBuliding 1,No.75 Xiangfeng Street, ",
        "city" : "Dongguan",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "Dongguan Chuangtong Shiji Technology Co.,Ltd",
      "managedByBusinessPartnerAmforiId" : "156-062153-000",
      "siteAmforiId" : "156-062153-001"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1747180800000,
    "beingReplanned" : false,
    "uuid" : "a3784ef2-f0ab-4bbf-80bc-914e1ea2ad85",
    "timeWindowFrom" : 1744588800000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "25-0319232",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FULL_MONITORING",
      "en_GB" : "Full Monitoring",
      "tr_TR" : "Tam Denetim",
      "zh_CN" : "全面监测活动"
    },
    "requestorLegalName" : "Miles",
    "requestDate" : 1743148187212,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743148187235
    },
    "esLastIndexedTimestamp" : 1743148187300
  }, {
    "monitoredSite" : {
      "name" : "Anjifast Co., Ltd",
      "address" : {
        "street" : "Xiaoshu Industrial Area  Anji, Zhejiang, China (zip code: 313307)",
        "zip" : "303307",
        "city" : "huzhou",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "Anjifast Co., Ltd",
      "managedByBusinessPartnerAmforiId" : "156-056740-000",
      "siteAmforiId" : "156-056740-001"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1747267200000,
    "beingReplanned" : false,
    "uuid" : "fd6de737-a1e8-4f87-bca5-8da9bca2f2e1",
    "timeWindowFrom" : 1744675200000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "25-0319217",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FULL_MONITORING",
      "en_GB" : "Full Monitoring",
      "tr_TR" : "Tam Denetim",
      "zh_CN" : "全面监测活动"
    },
    "requestorLegalName" : "Conmetall Meister GmbH",
    "requestDate" : 1743146149186,
    "announcementType" : {
      "key" : "AnnouncementType.SEMI_ANNOUNCED",
      "en_GB" : "Semi Announced",
      "tr_TR" : "Yarı Haberli",
      "zh_CN" : "半通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743146149198
    },
    "esLastIndexedTimestamp" : 1743146149294
  }, {
    "monitoredSite" : {
      "name" : "Yancheng Zhongrun Textile New Materials CO.,LTD",
      "localName" : "盐城中润纺织新材料有限公司91320921MA27KRU00E",
      "address" : {
        "street" : "Building 13 and 14，National Pioneer Park，Xiaojian Town，Xiangshui County",
        "zip" : "224611",
        "city" : "Yancheng ",
        "country" : {
          "key" : "Country.CN",
          "en_GB" : "China",
          "tr_TR" : "Çin",
          "zh_CN" : "中国"
        }
      },
      "monitoredPartyLegalName" : "Yancheng Zhongrun Textile New Materials CO.,LTD",
      "managedByBusinessPartnerAmforiId" : "156-047507-000",
      "siteAmforiId" : "156-047507-001"
    },
    "monitoringActivityName" : "amfori Social Audit - Manufacturing",
    "monitoringPartnerAmforiId" : "756-000001-000",
    "timeWindowTo" : 1749859200000,
    "beingReplanned" : false,
    "uuid" : "f4e9cb3f-5dc1-4a12-85d8-a9bd2f3ff149",
    "timeWindowFrom" : 1747180800000,
    "monitoringInitiative" : {
      "key" : "MonitoringInitiative.BSCI",
      "en_GB" : "BSCI",
      "tr_TR" : "BSCI",
      "zh_CN" : "BSCI"
    },
    "monitoringId" : "24-0257111-1",
    "replanned" : false,
    "monitoringType" : {
      "key" : "MonitoringType.FOLLOW_UP_MONITORING",
      "en_GB" : "Follow-up Monitoring",
      "tr_TR" : "Takip Denetimi",
      "zh_CN" : "跟进监测"
    },
    "requestorLegalName" : "Avec BV",
    "requestDate" : 1743144935454,
    "announcementType" : {
      "key" : "AnnouncementType.FULLY_UNANNOUNCED",
      "en_GB" : "Fully Unannounced",
      "tr_TR" : "Tamamen Habersiz",
      "zh_CN" : "不通知"
    },
    "currentState" : {
      "state" : {
        "key" : "monitoring.monitoring.partner.planning.state.to.confirm",
        "en_GB" : "To Confirm",
        "tr_TR" : "Onaylamak için",
        "zh_CN" : "确认"
      },
      "stateDate" : 1743144935472
    },
    "esLastIndexedTimestamp" : 1743144935540
  } ],
  "start" : 0,
  "totalItems" : 13
}
--------------Response end----------------


 - 以下登陆账号在.env中
AMFORI_USERNAME=你的用户名
AMFORI_PASSWORD=你的密码


 - Using ChromeDriver at: /opt/homebrew/bin/chromedriver




--------------------------------------------

需求二：



生成一个新的python程序，

需求：用上个程序中的取得的tocken,打开以下API-URL：
https://platform.amfori.org/v1/services/monitoring/monitoring-partner-plannings/f410af4b-ddf2-4c01-b4b5-cd2c740f16e0

1. 将返回的结果输出为表格，保存到一个Excel表格中。
2. 要求程序每次执行时，如果有新增就添加，如果有更新就更新内容，以'Site amfori ID'不主键判断是新增还是更新。
3. 如果有多页，就翻页抓取下一页的内容，直至全部抓取完成。
4. 在每个行中增加三列列，一列为新增创建时间，一列为更新时间（每次更新后，保存更新时间）,最后一列为抓取时间

------------- response begin--------------
{
  "uuid" : "f410af4b-ddf2-4c01-b4b5-cd2c740f16e0",
  "monitoringPartnerUuid" : "f13230fe-ae94-4afb-9d70-9f089c9cc05f",
  "version" : 4,
  "initiative" : "MonitoringInitiative.BEPI",
  "monitoringActivityName" : "amfori Environmental Monitoring",
  "announcementType" : "AnnouncementType.FULLY_ANNOUNCED",
  "requestDate" : "2025-01-03",
  "requestedTimeWindow" : {
    "from" : "2025-01-04",
    "fromDayPart" : "DayPart.MORNING",
    "to" : "2025-12-31",
    "toDayPart" : "DayPart.AFTERNOON"
  },
  "confirmedTimeWindow" : {
    "from" : "2025-01-06",
    "fromDayPart" : "DayPart.MORNING",
    "to" : "2025-12-31",
    "toDayPart" : "DayPart.AFTERNOON"
  },
  "unavailabilityDays" : [ ],
  "planningFailed" : false,
  "planned" : false,
  "toPlan" : true,
  "beingReplanned" : false,
  "replanned" : false,
  "toConfirm" : false,
  "waitingForUnavailabilityDays" : false,
  "currentState" : {
    "name" : "monitoring.monitoring.partner.planning.state.to.plan"
  },
  "monitoredSite" : {
    "siteAmforiId" : "704-000003-002",
    "name" : "Vinh Thong Producing Trading Service Co., Ltd",
    "address" : {
      "street" : "Lot III- 17, Group CN III, Road No. 13, Tan Binh Industrial Park, Tay Thanh Ward, Tan Phu Disctrict, HCMC, Viet Nam",
      "city" : "Ho Chi Minh",
      "stateProvince" : {
        "code" : "VN-SG",
        "name" : "StateProvince.VN-SG"
      },
      "country" : "Country.VN"
    },
    "localName" : "CÔNG TY TNHH SẢN XUẤT-THƯƠNG MẠI-DỊCH VỤ VINH THÔNG. Business license number: 0301414967",
    "workforce" : {
      "numberOfWorkers" : "251-550"
    },
    "monitoredPartyLegalName" : "Vinh Thong Producing Trading Service Co., Ltd",
    "monitoredPartyCompanyIdentifiers" : [ {
      "type" : "MonitoringCompanyIdentifierType.VAT_REGISTRATION_NUMBER",
      "value" : "0301414967"
    }, {
      "type" : "MonitoringCompanyIdentifierType.COMPANY_REGISTRATION_NUMBER",
      "value" : "01"
    }, {
      "type" : "MonitoringCompanyIdentifierType.BUSINESS_LICENCE_NUMBER",
      "value" : "0301414967"
    } ],
    "gicsSubIndustry" : "GICSSubIndustry.FOOTWEAR",
    "gs1ProductClasses" : [ ],
    "amforiProcessClassifications" : [ "AmforiProcessClassification.SEWING_STITCHING_12004" ],
    "contactDetails" : {
      "emailAddress" : "phuongloan@vithoco.com.vn",
      "phoneNumber" : "+84 28 3815 5178",
      "faxNumber" : "+84 28 3815 5179",
      "website" : "http://www.vithoco.com.vn"
    },
    "inWaterStressedRegion" : false,
    "managedByBusinessPartnerAmforiId" : "704-000003-000",
    "verified" : true,
    "siteType" : "OWN_SITE",
    "siteState" : {
      "state" : "SiteStateType.ACTIVE"
    }
  },
  "nextTierMonitoredSites" : [ ],
  "monitoringId" : "25-0303917",
  "teamEngagedMonitoringPersonNames" : [ ],
  "monitoringType" : "MonitoringType.FULL_MONITORING",
  "monitoringActivityScope" : "MonitoringActivityScope.ONE_SITE",
  "requestor" : {
    "uuid" : "036082bc-36bd-484b-aba5-305468535fe2",
    "legalName" : "Rieg & Niedermayer GmbH",
    "address" : {
      "street" : "Zillenhardtstr. 2/2",
      "zip" : "73037",
      "city" : "Göppingen",
      "stateProvince" : {
        "code" : "DE-BW",
        "name" : "StateProvince.DE-BW"
      },
      "country" : "Country.DE"
    },
    "contactDetails" : {
      "emailAddress" : "bayer@r-n.de",
      "phoneNumber" : "+49 7161 606910",
      "faxNumber" : "+49 7161 6069191"
    }
  },
  "monitoringScopes" : [ {
    "siteAmforiId" : "704-000003-002",
    "sectionsInScope" : [ {
      "sectionName" : "A - Monitoring Person",
      "forFollowUp" : false
    }, {
      "sectionName" : "B - Verification of Risk Assessment data",
      "forFollowUp" : false
    }, {
      "sectionName" : "EPA 1 - Environmental Management System",
      "forFollowUp" : false
    }, {
      "sectionName" : "EPA 2 - Energy & Climate",
      "forFollowUp" : false
    }, {
      "sectionName" : "EPA 3 - Emissions to Air",
      "forFollowUp" : false
    }, {
      "sectionName" : "EPA 4 - Water & Effluents",
      "forFollowUp" : false
    }, {
      "sectionName" : "EPA 5 - Waste",
      "forFollowUp" : false
    }, {
      "sectionName" : "EPA 6 - Biodiversity",
      "forFollowUp" : false
    }, {
      "sectionName" : "EPA 7 - Chemicals",
      "forFollowUp" : false
    }, {
      "sectionName" : "EPA 8 - Nuisances",
      "forFollowUp" : false
    } ]
  } ],
  "monitoringActivityFocusedScope" : false,
  "canBeReplanned" : false,
  "teamMonitoringPersonUuids" : [ ],
  "canRequestChangeToFullyAnnouncedMonitoring" : false
}
------------- response end--------------
 
需求三：
根据需求二的基础上，在保留需求二中生成的Excel中的sheet的同时，将返回的结果按以下要求生成到需求二中excel的另一个Sheet中。
说明一下，结果是要在一excel中保存存两个sheet.
要求程序每次执行时，如果有新增就添加，如果有更新就更新内容，以'Site amfori ID'不主键判断是新增还是更新。

表格列名	JSON 中对应字段和数据
Request Date	"requestDate" : "2025-01-03",
Site amfori ID	"siteAmforiId" : "704-000003-002",
Producer Name	"monitoredSite" : {"name" : "Vinh Thong Producing Trading Service Co., Ltd", ...} 中 "name" 字段对应的值为 "Vinh Thong Producing Trading Service Co., Ltd"
Contact Email	"monitoredSite" : {"contactDetails" : { "emailAddress" : "phuongloan@vithoco.com.vn", ...} } 中 "emailAddress" 字段对应的值为 "phuongloan@vithoco.com.vn"
Unavailability Days	"unavailabilityDays" : [ ],
Audit Announcement	"announcementType" : "AnnouncementType.FULLY_ANNOUNCED",
 
需求四：
是需求一个变更需求，对amfori_scraper.py进行修改，不要修改任何已存在的逻辑，只添加以下需求
1. 将'Link'列改名为“To_Confirm_Link”
2. 在需求一个输出结果中增加一列，在"To_Confirm_Link"列之后加一列名为“To_Plan_Link”
3. To_Plan_Link列的URL如下：https://platform.amfori.org/v1/services/monitoring/monitoring-partner-plannings/f410af4b-ddf2-4c01-b4b5-cd2c740f16e0
4. 更新“To_Confirm_Link”和“To_Plan_Link”中的ID为uuid
5. 只有数据列“Status”状态为“已确认”的，才生成“To_Confirm_Link”中的URL

需求五：

修改amfori_detail_scraper.py，需求如下：
在程序中不要打开这个URL：https://platform.amfori.org/v1/services/monitoring/monitoring-partner-plannings/f410af4b-ddf2-4c01-b4b5-cd2c740f16e0
修改为读取Excel(amfori_data.xlxs)，找到Excel表中列名为“Status_comparation“中的值为”已确认“的所有记录，读取表格中的列“to_confirm_link”的URL，并循环遍例所有的URL，将URL一个一个替换第1点中的URL,执行amfori_detail_scraper.py后面的逻辑

需求六：
amfori_detail_scraper.py执行成功后，将Excel(amfori_data.xlxs)中的循环遍例过的所有的URL对应的行中的Status_comparation的记录更新成为“Extracted"



需求七：

修改amfori_detail_scraper.py，不要修改其他逻辑，只增加以下需求：

https://platform.amfori.org/v1/services/monitoring/monitoring-partner-plannings/57a05cff-9cfc-4273-91a8-5198c6c6810a

读取每个URL页面中的内容，输出为表格amfori_detail_data.xlxs，以下是希望输出的表格字段和URL输出后的JSON中的内容的对应关系。请解析并将内容输出到Requirement3 Data（Sheet）中

每一列为以下格式：
Request Date： ----------   "requestDate" : "2025-03-28",
Site amfori ID： ----------  "monitoredSite" ->   "siteAmforiId" : "156-035945-002",
Monitoring ID： ----------    "monitoringId" : "24-0250779-1",
Company Name(LegalName)： ---------- "monitoredSite"->"monitoredPartyLegalName" : "Quanzhou Junyang trade IMP. & EXP. CO LTD.",
Site Name(Sitename)： ---------- "monitoredSite"->"name" : "Mao Fa Toys And Gift Corporation Ltd",
Local Name(Localname)： ---------- "monitoredSite"->"localName" : "泉州市茂发玩具礼品有限公司(913505217531209207)",
Contact Email： ---------- "contactDetails" ->"emailAddress" : "438975228@qq.com",
Contact Phonenumber: ---------- "contactDetails" ->"phoneNumber" : "+8659522505987",
address:  ----------  "monitoredSite" -> "address" :
Audit Start window(confirmedTimeWindow-from)： ---------- "confirmedTimeWindow"->"from" : "2025-01-06",
Audit To window(confirmedTimeWindow-to)： ---------- "confirmedTimeWindow"->"to" : "2025-12-31",
Status： ---------- ""
Audit Start date： ---------- ""
Audit End date： ---------- ""
Unavailability Days： ---------- "unavailabilityDays" : [ ],
Schedule#： ---------- ""
Job#： ---------- ""
BSCI MEMBER： ----------   "requestor" -> "legalName" : "El Corte Inglés,S.A",
BSCI Member phonenumber: ： ----------   "requestor" -> "contactDetails" -> "phoneNumber" : "+34914018500",
BSCI Member emailAddress: ： ----------   "requestor" -> "contactDetails" -> "emailAddress" : "+34914018500",
Audit Announcement： ----------  "announcementType" : "AnnouncementType.SEMI_ANNOUNCED",
Audit Methodology： ----------   "monitoringActivityName" : "amfori Social Audit - Manufacturing",
Audit type： ---------- "monitoringType" : "MonitoringType.FOLLOW_UP_MONITORING",
CS： ---------- ""
Remark（平台来单or CS来单）： ---------- ""
Related Sales ： ---------- ""


需求九：
@amfori_detail_scraper.py 现在需要做一个增强功能，每次执行这个程序前，先将数据备份，备的方法是将amfori_detail_data.xlxs中的数据，追加到另一个excel中，名字就定为amfori_detail_data_backup.xlxs，这个文件结构和amfori_detail_data.xlxs完全一样，不能被删除，每次只能追加数据，要增加一列名为“备份时间”，将每次追加的时间记下来。如果是第一次这个文件不存在，就创建一个。

需求十：
请重构amfori_scraper.py, 将登陆和取得tocken部分独立出来，然后分成两部执行：
1. 只完成登陆和取得tocken功能。
2. 将取得的tocken用来执行后续的数据抓取工作。
3. 这样拆分的目的是不希望每次都重新登陆，期望的效果是，每次执行前，判断tocken是否有效，如有效，则不用重新登陆，减少登陆的次数。
4. 不能修改原代码的逻辑

需求十一：
请重构amfori_detail_scraper.py, 将登陆和取得tocken部分独立出来，然后分成两部执行：
1. 只完成登陆和取得tocken功能。
2. 将取得的tocken用来执行后续的数据抓取工作。
3. 这样拆分的目的是不希望每次都重新登陆，期望的效果是，每次执行前，判断tocken是否有效，如有效，则不用重新登陆，减少登陆的次数。
4. 不能修改原代码的逻辑

需求十二：
请重构amfori_detail_scraper.py, 增加另一个入口：
1.修改程序，增加一个入口，保留原逻辑正常在执行的入口。
2. 增加的入口是，提示用户输入参数，参数为多个“siteAmforiId”，以‘：’相隔可以一次性输入多个siteAmforiId。
3. 如果有参数输入，则按照输入的siteAmforiId列表，循环一个一个调用程序查询excel（amfori_data.xlxs）的列“Site amfori ID”中否有对应的siteAmforiId。
4. 按照查询到的“Site amfori ID”对应的“To_Plan_Link”中的URL，重新抓取URL数据，并将结果更新到amfori_detail_data.xlxs中。
5. 如没有查询到，执行完所在的Site amfori ID后，提示用户未找到对应的Site amfori ID（如果多个未找到，提示多个Site amfori ID）
6. 原有代码的逻辑不变，只是按要求增加一个入口调用。

需求十三：
修改app.py和index.html, 让他也支持调用需求十二中提到的入口；
需要增加一个输入框，让用户输入多个“siteAmforiId”，以‘：’相隔可以一次性输入多个siteAmforiId。
执行时Run detail Scraper时，判断如果输放框不为空，执行入口2，否则执行入口1

需求十四：
修改app.py和index.html,如果用户输入的是多个“siteAmforiId”，以‘：’相隔可以一次性输入多个siteAmforiId。
增加一个按钮，名为“Run Detail Scraper with ID”, 在点这个按钮前，判断输入框是否为空，如为空，提示用户需要先输入siteAmforiId，并提示规则,如不为空，执行入口2；
修改原按钮“Run Detail Scraper”， 只用来执行在入口1，没有参数的数据抓取工作

需求十五：
修改amfori_scraper.py, 要求将每次抓取的数据的状态输出出来，其他原逻辑保持不变，现在的输出如下：
-----
Starting amfori scraper...

Setting up Chrome driver...
Using ChromeDriver at: /opt/homebrew/bin/chromedriver
ChromeDriver initialized successfully
WebDriverWait initialized with 30 second timeout
Token is valid
Using existing valid token
Fetching data from offset 0...
Extracting data from response...
Extracted data for site: YIWU SAIQIAO JEWELRY CO., LTD
Extracted data for site: Wangjiang Sansheng Garments Co., Ltd.
Extracted data for site: 东莞市捷进安防用品有限公司
Extracted data for site: Huidong Hua Xin Industrial Co., Ltd.
Extracted data for site: Pujiang Chiyuan Industry and Trade Co., Ltd
Extracted data for site: Jiangxi Jiayinking Culture Technology Company Limited.
Extracted data for site: NINGBO YIBAI CHILDREN PRODUCTS CO., LTD
Extracted data for site: IDELITA（Chuzhou)  crystal glass co.,Itd
Extracted data for site: THE FIRST BRANCH OF FOSHAN CITY SHUNDE DISTRICT JIAHE INDUSTRIAL CO., LTD
Extracted data for site: Yunhe Fenglin crafts Co., LTD
Extracted data for site: Ningbo Oriental Prosperity Photoelectric Technology Co.,Ltd
Extracted data for site: Guilin Bamboo Forever Technology Co., Ltd
Extracted data for site: Yangzhou Aolikes Sports Goods Co., Ltd.
Extracted data for site: Ninghai Nade Commodity Limited Company
Extracted data for site: Dongtai Electronic Technology (Suzhou) Co., Ltd
Extracted data for site: Dongguan Chuangtong Shiji Technology Co.,Ltd
Extracted data for site: Anjifast Co., Ltd
Extracted data for site: Tiantai Tiandong Auto Accessories Co., Ltd.
Extracted data for site: CHANGZHOU SHOUCHEN TOOLS MANUFACTURE CO ., LTD
Extracted data for site: Yancheng Zhongrun Textile New Materials CO.,LTD
Extracted data for site: NCIF( LinYi) Geosynthetics Co.,Ltd

Scraping Status Summary:

Scraping completed successfully!
-----
我期望的效果是这样子的：
-----
Starting amfori scraper...

Setting up Chrome driver...
Using ChromeDriver at: /opt/homebrew/bin/chromedriver
ChromeDriver initialized successfully
WebDriverWait initialized with 30 second timeout
Token is valid
Using existing valid token
Fetching data from offset 0...
Extracting data from response...
New： 6；
  Extracted data for site: YIWU SAIQIAO JEWELRY CO., LTD
  Extracted data for site: Wangjiang Sansheng Garments Co., Ltd.
  Extracted data for site: 东莞市捷进安防用品有限公司
  Extracted data for site: Huidong Hua Xin Industrial Co., Ltd.
  Extracted data for site: Pujiang Chiyuan Industry and Trade Co., Ltd
  Extracted data for site: Jiangxi Jiayinking Culture Technology Company Limited.
Update： 8；
  Extracted data for site: NINGBO YIBAI CHILDREN PRODUCTS CO., LTD
  Extracted data for site: IDELITA（Chuzhou)  crystal glass co.,Itd
  Extracted data for site: THE FIRST BRANCH OF FOSHAN CITY SHUNDE DISTRICT JIAHE INDUSTRIAL CO., LTD
  Extracted data for site: Yunhe Fenglin crafts Co., LTD
  Extracted data for site: Ningbo Oriental Prosperity Photoelectric Technology Co.,Ltd
  Extracted data for site: Guilin Bamboo Forever Technology Co., Ltd
  Extracted data for site: Yangzhou Aolikes Sports Goods Co., Ltd.
  Extracted data for site: Ninghai Nade Commodity Limited Company
  Extracted data for site: Dongtai Electronic Technology (Suzhou) Co., Ltd
Confirmed：6；
  Extracted data for site: Dongguan Chuangtong Shiji Technology Co.,Ltd
  Extracted data for site: Anjifast Co., Ltd
  Extracted data for site: Tiantai Tiandong Auto Accessories Co., Ltd.
  Extracted data for site: CHANGZHOU SHOUCHEN TOOLS MANUFACTURE CO ., LTD
  Extracted data for site: Yancheng Zhongrun Textile New Materials CO.,LTD
  Extracted data for site: NCIF( LinYi) Geosynthetics Co.,Ltd

Scraping Status Summary:

Scraping completed successfully!

-------------------
ersion 2

需求V2-0001:
1. 现需要升级一下程序amfori_scraper.py和amfori_detail_scraper.py, 将Excel换成数据库，建议采用sqllite为数据库
2. 表结构和现有的三个excel保持一致
3. 需要在每一张表增加一个主键，要求用数字自增长的形式
4. 现在Excel中的列名中如果有空格，需要更新为以下划张连接的形式，例：“Site amfori ID” 转为 “Site_amfori_ID”
5. 请不要修改任何原代码中的逻辑，只升级将数据从Excel改为Sqllite中
6. 2. 重构amfori_scraper.py和amfori_detail_scraper.py, 将数据库访问和操作部分形成独立的文件，以供两个程序调用，为未来扩展更多的数据库操作打下基础



需求V2-0002:
1. 不要修改amfori_scraper.py和amfori_detail_scraper.py
2. 新增页面可查询三个表格中内容，要求可以分页查询，每页可以看的记录数可以自己设置。
3. 每个查询页面都需要有查询条件，暂定为Site amfori ID
4. 在index.html 和新增的query.html, 增加相互导航功能
5. 生成三个tab标签查询
6. 点击不同的tab执行查询不同的表中的内容
7. 表将查询结果按照以下字段顺序显示到查询页面中：
    Table: amfori_detail_data_backup
    backup_id, site_detail_id, Scraped_At, Status, Request_Date, Site_amfori_ID, Monitoring_ID, Company_Name_LegalName, Site_Name_Sitename, Local_Name_Localname, Contact_Email, Contact_Phonenumber, address, Audit_Start_window_from, Audit_To_window_to, Status1, Audit_Start_date, Audit_End_date, Unavailability_Days, Schedule_Number, Job_Number, BSCI_MEMBER, BSCI_Member_phonenumber, BSCI_Member_emailAddress, Audit_Announcement, Audit_Methodology, Audit_type, CS, Remark, Related_Sales, Created_At, Updated_At, Backup_Time
    Table: site_details
    id, Scraped_At, Status, Request_Date, Site_amfori_ID, Monitoring_ID, Company_Name_LegalName, Site_Name_Sitename, Local_Name_Localname, Contact_Email, Contact_Phonenumber, address, Audit_Start_window_from, Audit_To_window_to, Status1, Audit_Start_date, Audit_End_date, Unavailability_Days, Schedule_Number, Job_Number, BSCI_MEMBER, BSCI_Member_phonenumber, BSCI_Member_emailAddress, Audit_Announcement, Audit_Methodology, Audit_type, CS, Remark, Related_Sales, Created_At, Updated_At
    Table: sites
    id, Site_amfori_ID, Site_Name, Local_Name, Address_Street, Address_City, Address_Zip, Address_Country, Address1, Legal_Name, Initiative, Status, Monitoring_ID, Monitoring_Type, Announcement_Type, Requestor, Request_Date, State_Date, To_Plan_Link, to_confirm_link, Created_At, Updated_At, Scraped_At, Status_comparation


需求V2-0003:
入口1，现在执行不对，条件是查询sites表中记录为Confirmed记录，根据该记录中的URL，抓取数据，抓取成功后，将结果保存在site_detail中，并且更新状态，第一次为New，第二次及以上为Updated。同是将更新时间和抓取时间更新为最新的时间

需求V2-0004:
@amfori_detail_scraper.py 现在需要做一个增强功能，每次执行这个程序前，包括入口1和入口2，先将数据备份，只备份每次被新增或更新的数据，没有被影响或修改的记录不被备份，备的方法是将site_detail中的数据，追加到另一个表中，名字就定为amfori_detail_data_backup，这个表结构和site_details一样：
1. 要增加一列名为“备份时间”，将每次追加的时间记下来。
2. 要增加一列为主键ID，唯一且自增，
3. 原site_detail表的ID只是一个数据，不再是主键；
4. 每次备份时，一定不能删除已有数据，每次只能追加数据。
5. 在备份数据时有个问题，现在备份表中没有site_detail中的ID， 需要增加一列将site_detail中的ID也放到备份表中，同时不应该是主键，名字可以定个site_detail_ID


-------------------

需求V3:

V0.1
1. 请参考amfori_scraper.py, 创建一个新的爬取程序，名为amfori_confirmed_scraper.py, 取得tocken的逻辑不变，只将查询URL及查询条件更换为以下URL中的查询条件。
2. 这个URL返回的JSON，如@toPlan.json.
3. 请将返回的信息JSON转为table并保存在Excel表中
4. URL： 
https://platform.amfori.org/v1/services/monitoring/monitoring-partner-plannings/to-plan/search?childQuery=&parentQuery=%2B(+monitoringInitiative.en_GB:BSCI+)+%2B(+currentState.state.en_GB:Waiting%5C+for%5C+Unavailability%5C+Days+currentState.state.en_GB:To%5C+Plan+)&rows=25&sort=&sortOrder=&start=0


https://platform.amfori.org/v1/services/monitoring/monitoring-partner-plannings/planned/search?childQuery=&parentQuery=%2B(+monitoredSite.address.country.en_GB:China+)+%2B(+currentState.state.en_GB:Expired+currentState.state.en_GB:Canceled+)+%2B(+monitoringInitiative.en_GB:BSCI+)&rows=25&sort=&sortOrder=&start=0

https://platform.amfori.org/v1/services/monitoring/monitoring-partner-plannings/to-plan/search?childQuery=&parentQuery=%2B(+monitoringInitiative.en_GB:BSCI+)+%2B(+currentState.state.en_GB:Waiting%5C+for%5C+Unavailability%5C+Days+currentState.state.en_GB:To%5C+Plan+currentState.state.en_GB:Expired+currentState.state.en_GB:Canceled+)&rows=25&sort=&sortOrder=&start=0


V0.2
1. 请参考amfori_scraper.py, 创建一个新的爬取程序，名为amfori_confirmed_scraper_by_IDlist.py, 取得tocken的逻辑不变;
2. 这个查询只是取得一个siteAmforiId的查询，要求可以一次性输入多个siteAmforiId，循环用不同的siteAmforiId调用这个URL。将查询取得的结果保存到一个excel中。
3. 这个URL返回的JSON，如@toPlan_single.json.
https://platform.amfori.org/v1/services/monitoring/monitoring-partner-plannings/to-plan/search?childQuery=&parentQuery=%2BmonitoredSite.siteAmforiId:(*156%5C-004887%5C-002*)&rows=25&sort=&sortOrder=&start=0


请按requirement.md中的这段需求生成新的python程序

V0.3
1. 请参考amfori_detial_scraper.py, 创建一个新的爬取程序，名为amfori_confirmed_detail_scraper_by_IDlist.py, 取得tocken的逻辑不变;
2. 根据amfori_to_plan_data_by_id.xlxs中的数据，按amfori_detial_scraper.py中的逻辑将数（从Excel中的To_Plan_Link）据抓取到新的Excel中。
3. 这个查询只是取得一个siteAmforiId的查询，要求可以一次性输入多个siteAmforiId，循环用不同的siteAmforiId调用这个URL。将查询取得的结果保存到一个excel中。


v0.4
1. 修改amfori_confirmed_detail_scraper_by_IDlist.py中的逻辑：
2. 如果返回的JSON中 "waitingForUnavailabilityDays" : true,值为true，则'Unavailability Days'显示“waiting For Unavailability Days”。
3. 否则正常取得"unavailabilityDays" : [ ]的值
'Unavailability Days': unavailability_days_str,中的逻辑

v0.5
1. 取得待确认的列表 - 确认表 - 状态为New
2. 确认 - 如确认 - 状态为confirm - 确认表
3. 抓取确认的数据 - 如已抓取过，状态变为已抓取 - Exracted. - 详细数据抓取表
4. 需要能重复抓取 - 输入ID列表重复抓取 - 详细抓取表
5. 


V0.6
修改这一部分代码，判断excelj否存在，如不存在创建，并将数据写到代码定义的Data sheet名字中。如存在，则打开Excel，并创建新的data sheet,如datasheet存在，则删除原有数据，再将数据写入