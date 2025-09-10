// i18n.js

// 1) 文案字典（按你的页面实际内容补全/修改 key）
const dict = {
  zh: {
    "Biography": "<b>简介</b>",
    "Milestone": "<b>里程碑</b>",
    "Honors": "<b>主要荣誉</b>",
    "Publications": "<b>出版物</b>",
    "Teaching": "<b>教学&学术服务</b>",
    "Misc": "<b>其他</b>",
    "College": "浙江大学 计算机科学与技术学院",

    "Hello": "您好，我叫张道泽，目前正在<a href='https://www.zju.edu.cn/english/'>浙江大学</a>攻读硕士学位，有幸在<a href='http://yangy.org/'>杨洋</a>教授的指导下于<a href='http://www.dcd.zju.edu.cn/'>DCD实验室</a>开展研究。我的研究兴趣包括深度学习和数据挖掘在医疗保健领域以及时间序列分析中的应用。此外，我还在积极探索大语言模型和多模态语言模型领域的前沿技术。如果您正在寻找任何形式的学术合作，欢迎您随时与我联系。此外，我目前正在寻求工业界的工作机会。如果您有任何指引，请随时与我联系，非常感谢！",    "Research": "研究方向",
    "Machine": "医疗健康领域的人工智能",
    "Time": "时间序列分析",
    "Multimodal": "(多模态)大语言模型",
    "Recommendation": "推荐系统",
    
    "Education": "教育经历",
    "Zhejiang": "浙江大学",
    "Academic": "学术型硕士，人工智能研究所，计算机学院，26届",
    "Bachelor": "学士，计算机科学与技术，计算机学院，23届",
    "Xi": "西安市铁一中学",
    "Hua": "华罗庚理科菁英班，19届 ",

    "timeline1": "<div class='timeline-date'> 2019年9月 </div> <div class='timeline-title'> 录取 </div> <div class='timeline-desc'> 被浙江大学<a href='http://ckc.zju.edu.cn/ckcen/'>竺可桢学院</a>求是科学班（物理）录取 </div>",
    "timeline2": "<div class='timeline-date'> 2020年9月 </div> <div class='timeline-title'> 转专业 </div> <div class='timeline-desc'> 被浙江大学<a href='http://www.cs.zju.edu.cn/csen/'>计算机学院</a>计算机科学与技术专业录取 </div>",
    "timeline3": "<div class='timeline-date'> 2021年7月 </div> <div class='timeline-title'> 荣誉 </div> <div class='timeline-desc'> 浙江省政府奖学金 </div> <div class='timeline-desc'> 浙江大学一等学业奖学金 </div> <div class='timeline-desc'> 陈天洲教育基金优秀学生奖学金 </div>",
    "timeline5": "<div class='timeline-date'> 2023年7月 </div> <div class='timeline-title'> 荣誉 </div> <div class='timeline-desc'> 浙江省优秀本科毕业生 </div> <div class='timeline-desc'> 浙江大学优秀本科毕业生 </div>",
    "timeline6": "<div class='timeline-date'> 2023年9月 </div> <div class='timeline-title'> 研究 </div> <div class='timeline-desc'> <b>1篇论文</b>被NeurIPS 2023接收 (<b>第一作者</b>) </div> <div class='timeline-desc'> <b>1篇论文</b>被NeurIPS 2023接收 (<b>共同第一作者</b>) </div>",
    "timeline7": "<div class='timeline-date'> 2024年5月 </div> <div class='timeline-title'> 研究 </div> <div class='timeline-desc'> <b>1篇论文</b>被SIGKDD 2024接收 (<b>第一作者</b>) </div> <div class='timeline-desc'> <b>1篇论文</b>挂在arXiv (<b>第二作者</b>) </div>",
    "timeline8": "<div class='timeline-date'> 2024年10月 </div> <div class='timeline-title'> 荣誉 </div> <div class='timeline-desc'> 以人工智能研究所硕士第一名获得国家奖学金 </div>",

    "honor10": "国家奖学金，2024年（人工智能研究所硕士第一名，前1%）",
    "honor9": "浙江大学优秀研究生，2024年",
    "honor8": "浙江省优秀本科毕业生，2023年（前5%）",
    "honor7": "小米奖学金，2022年",
    "honor6": "浙江省政府奖学金，2021年（前3%）",
    "honor5": "浙江大学一等奖学金，2021年（前3%）",
    "honor4": "陈天洲教育基金优秀学生奖学金，2021年",
    "honor3": "浙江大学优秀学生，2021年", 
    "honor2": "浙江省大学生物理竞赛一等奖，2020年（前5%）",
    "honor1": "浙江大学优秀共青团员，2020年",

    "direction1": "医疗健康领域的人工智能",
    "direction2": "大语言模型",

    "Conference": "学术会议",
    "NeurIPS25": "在NeurIPS 2025担任Program committee member",
    "KDD24": "在KDD 2024作口头报告介绍Brant-X论文",
    "Teaching Assistant": "教学助教",
    "CS 21121340": "CS 21121340: <i>计算机网络</i>，与<a href='https://person.zju.edu.cn/0097159/744726.html'>陆系群</a>教授（2023年）",
    "CS 21121340": "CS 21121340: <i>计算机网络</i>，与<a href='https://person.zju.edu.cn/0097159/744726.html'>陆系群</a>教授（2022年）",
    "Peer": "朋辈辅学导师",
    "CS 211C0010": "CS 211C0010: <i>面向对象程序设计</i>，与<a href='https://person.zju.edu.cn/0015060'>许威威</a>教授（2021年）",
    "CS 211G0280": "CS 211G0280: <i>C语言程序设计基础</i>（2020年）",

    "life": "生活中，我热爱历史🏺、地理🌎和古典音乐🎼，也学习过篆刻、国画等传统艺术🎨。13岁时，我有幸获得在美国举办的和平杯青少年书画大赛金奖🥇。",
    "student_union": "在竺可桢学院学生会工作的两年，我担任过文艺部副部长的职务。期间，我爱上了组织和策划一切与活动和表演相关的事务🌟。和团队成员一起，我负责组织了多次歌手大赛、新年晚会、毕业晚会等大型文艺活动。",
    "video_clip": "此外，我有幸担任过浙江大学英文版《后浪》的视频剪辑🎬工作，该作品获得了包括<a href='https://zj.zjol.com.cn/news.html?id=1442314'>浙江新闻</a>、<a href='https://www.thehour.cn/news/368090.html'>钱江晚报</a>、<a href='https://mp.weixin.qq.com/s?__biz=MzAxNjA1NTgzOA==&mid=2651352704&idx=2&sn=4bde99994165e5c8858d086eb12e3a7e&chksm=800665f1b771ece7f3a2e32f0d9fd94c896bb831c227e2aef7f2b0c67d10ecdd60e6cca0ae7f&scene=27'>外语教学与研究出版社</a>、新浪、搜狐等多家媒体和机构的认可与推广。<a href='https://www.bilibili.com/video/BV18Z4y1s7JK/?vd_source=bcb72b08d031075a66a8b31572c0c798'><img src='https://img.shields.io/badge/dynamic/json?label=views&style=social&logo=bilibili&query=$.data.stat.view&url=https://api.bilibili.com/x/web-interface/view?bvid=BV18Z4y1s7JK' alt='bilibili'> </a>",
},
  en: {
    "Biography": "<b>Biography</b>",
    "Milestone": "<b>Milestone</b>",
    "Honors": "<b>Honors & Awards</b>",
    "Publications": "<b>Publications</b>",
    "Teaching": "<b>Teaching</b>",
    "Misc": "<b>Misc</b>",
    "College": "College of Computer Science, ZJU",

    "Hello": "Hello, my name is Daoze Zhang and I am currently pursuing a Master's degree in <a href='https://www.zju.edu.cn/english/'>Zhejiang University</a>, fortunately advised by <a href='http://yangy.org/'>Prof. Yang Yang</a> in <a href='http://www.dcd.zju.edu.cn/'>DCD Lab</a>. My research interests include deep learning and data mining in the healthcare field and for time series analysis. Additionally, I am actively exploring more cutting-edge technologies in the field of large language models and multimodal language models. If you are looking for any form of academic cooperation, please feel free to touch me. <b>Futhermore, I am currently seeking job opportunities in industry. Please do not hesitate to contact me if you have any leads.</b> Thank you!",
    "Research": "Research Topics",
    "Machine": "Machine Learning for Healthcare",
    "Time": "Time Series Analysis",
    "Multimodal": "(Multimodal) Large Language Models",
    "Recommendation": "Recommendation System",

    "Education": "Education",
    "Zhejiang": "Zhejiang University",
    "Academic": "Academic Master, AI Institute, College of CS, 26'",
    "Bachelor": "Bachelor, Computer Science, College of CS, 23'",
    "Xi": "Xi'an Tieyi High School",
    "Hua": "Hua Luogeng Science Elite Class, 19'",

    "timeline1": "<div class='timeline-date'> Sept. 2019 </div> <div class='timeline-title'> Admission </div> <div class='timeline-desc'> Admitted to the Qiushi Science Class (Physics) at <a href='http://ckc.zju.edu.cn/ckcen/'>Chu Kochen Honors College</a>, ZJU </div>",
    "timeline2": "<div class='timeline-date'> Sept. 2020 </div> <div class='timeline-title'> Admission </div> <div class='timeline-desc'> Admitted to the <a href='http://www.cs.zju.edu.cn/csen/'>Computer Science</a> major at ZJU </div>",
    "timeline3": "<div class='timeline-date'> Jul. 2021 </div> <div class='timeline-title'> Awards </div> <div class='timeline-desc'> Zhejiang Provincial Government Scholarship </div> <div class='timeline-desc'> First-class Scholarship of ZJU </div> <div class='timeline-desc'> Outstanding Student Scholarship of CTZ Edu Fdn </div>",
    "timeline5": "<div class='timeline-date'> Jul. 2023 </div> <div class='timeline-title'> Awards </div> <div class='timeline-desc'> Outstanding Undergraduate Graduate of Zhejiang Province </div> <div class='timeline-desc'> Outstanding Undergraduate Graduate of ZJU </div>",
    "timeline6": "<div class='timeline-date'> Sept. 2023 </div> <div class='timeline-title'> Research </div> <div class='timeline-desc'> <b>1 paper</b> accepted by NeurIPS 2023 (<b>first author</b>) </div> <div class='timeline-desc'> <b>1 paper</b> accepted by NeurIPS 2023 (<b>co-first author</b>) </div>",
    "timeline7": "<div class='timeline-date'> May. 2024 </div> <div class='timeline-title'> Research </div> <div class='timeline-desc'> <b>1 paper</b> accepted by SIGKDD 2024 (<b>first author</b>) </div> <div class='timeline-desc'> <b>1 paper</b> posted on arXiv preprint (<b>second author</b>) </div>",
    "timeline8": "<div class='timeline-date'> Oct. 2024 </div> <div class='timeline-title'> Awards </div> <div class='timeline-desc'> National Scholarship </div> <div class='timeline-desc'> as 1st place among Masters of the AI Institute </div>",

    "honor10": "National Scholarship, 2024 (1st place among Masters of the AI Institute, Top 1%)",
    "honor9": "Outstanding Postgraduate Students of Zhejiang University, 2024",
    "honor8": "Outstanding Undergraduate Graduate of Zhejiang Province, 2023 (Top 5%)",
    "honor7": "Xiaomi Scholarship, 2022",
    "honor6": "Zhejiang Provincial Government Scholarship, 2021 (Top 3%)",
    "honor5": "First-class Scholarship of Zhejiang University, 2021 (Top 3%)",
    "honor4": "Outstanding Student Scholarship of CTZ Education Foundation, 2021",
    "honor3": "Outstanding Student of Zhejiang University, 2021", 
    "honor2": "First Prize in the Zhejiang Province College Physics Competition, 2020 (Top 5%)",
    "honor1": "Outstanding Youth League Member of Zhejiang University, 2020",

    "direction1": "AI for Healthcare: Deep Learning on Neural Signals",
    "direction2": "Large Language Models: Automatic Review of Documents",

    "Conference": "Conference",
    "NeurIPS25": "Program committee member of NeurIPS 2025",
    "KDD24": "Oral presentation at KDD 2024 to introduce the paper of Brant-X",
    "Teaching Assistant": "Teaching Assistant",
    "CS 21121340": "CS 21121340: <i>Computer Networks</i>, with <a href='https://person.zju.edu.cn/0097159/744726.html'>Prof. Xiqun Lu</a> (2023)",
    "CS 21121340": "CS 21121340: <i>Computer Networks</i>, with <a href='https://person.zju.edu.cn/0097159/744726.html'>Prof. Xiqun Lu</a> (2022)",
    "Peer": "Peer Tutoring Mentor",
    "CS 211C0010": "CS 211C0010: <i>Object-oriented Programming</i>, with <a href='https://person.zju.edu.cn/0015060'>Prof. Weiwei Xu</a> (2021)",
    "CS 211G0280": "CS 211G0280: <i>Fundamentals of C Programming</i> (2020)",
    
    "life": "In life, I have a passion for history🏺, geography🌎, and classical music🎼. I have also studied traditional arts such as seal carving and Chinese painting🎨. At the age of 13, I was honored to receive the gold medal🥇 in the Peace Cup Youth Painting and Calligraphy Competition held in the United States.",
    "student_union": "During my two years as a member and deputy minister of the Arts Department in CKC Honors College Student Union, I fell in love with organizing and managing everything related to events and performances🌟. Together with the team members, I was responsible for organizing multiple singing competitions, New Year's ceremonies, and graduation ceremonies. ",
    "video_clip": "Furthermore, I have had the opportunity to take on the role of video editing🎬 for the <i>ZJU English version of 'The Wave'</i>, which garnered recognition and promotion from various institutions including <a href='https://zj.zjol.com.cn/news.html?id=1442314'>Zhejiang News</a>, <a href='https://www.thehour.cn/news/368090.html'>Qianjiang Evening News</a>, <a href='https://mp.weixin.qq.com/s?__biz=MzAxNjA1NTgzOA==&mid=2651352704&idx=2&sn=4bde99994165e5c8858d086eb12e3a7e&chksm=800665f1b771ece7f3a2e32f0d9fd94c896bb831c227e2aef7f2b0c67d10ecdd60e6cca0ae7f&scene=27'>Foreign Language Research Press</a>, Sina, Sohu, and more. <a href='https://www.bilibili.com/video/BV18Z4y1s7JK/?vd_source=bcb72b08d031075a66a8b31572c0c798'> <img src='https://img.shields.io/badge/dynamic/json?label=views&style=social&logo=bilibili&query=$.data.stat.view&url=https://api.bilibili.com/x/web-interface/view?bvid=BV18Z4y1s7JK' alt='bilibili'> </a>",
}
};

// 2) 读取/设置当前语言（默认英文）
localStorage.clear(); 
const getLang = () => localStorage.getItem("lang") || "en";
const setLang = (lang) => localStorage.setItem("lang", lang);

// 3) 应用翻译：文本节点或指定属性
function applyI18n(lang) {
  const table = dict[lang] || {};
  // 替换元素文本
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    const attr = el.getAttribute("data-i18n-attr"); // e.g. "placeholder", "title", "alt", "content"
    const val = table[key];
    if (val == null) return; // 未找到 key 则跳过

    if (attr) {
      // 翻译属性（如 placeholder、title、alt、content 等）
      el.setAttribute(attr, val);
      // 对 <title> 特判（它是元素文本，不是属性）
      if (el.tagName === "TITLE") el.innerHTML = val;
    } else {
      // 替换可见文本，不动内部结构（保留子标签）
      // 常见做法：仅替换 textContent
      el.innerHTML = val;
    }
  });

  // 更新 <html lang="..."> 便于无障碍/SEO
  document.documentElement.setAttribute("lang", lang);
}

// 4) 绑定按钮
function initI18n() {
  const current = getLang();
  applyI18n(current);

  const btn = document.getElementById("langToggle");
  if (btn) {
    btn.addEventListener("click", () => {
      const next = getLang() === "zh" ? "en" : "zh";
      setLang(next);
      applyI18n(next);
      // 可选：更新按钮文案
      btn.textContent = next === "zh" ? "中文 / EN" : "EN / 中文";
      btn.setAttribute("aria-label", next === "zh" ? "切换语言" : "Toggle language");
    });
  }
}

document.addEventListener("DOMContentLoaded", initI18n);
