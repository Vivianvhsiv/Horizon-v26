import json
from pathlib import Path
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(page_title="Horizon", page_icon="✦", layout="wide")

APP_DIR = Path(__file__).parent

def find_data_file(filename: str) -> Path:
    """Find project data whether uploaded under data/ or repository root."""
    candidates = (APP_DIR / "data" / filename, APP_DIR / filename)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    searched = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(
        f"Required data file '{filename}' was not found. Checked: {searched}"
    )

DATA_FILE = find_data_file("majors.json")
with DATA_FILE.open(encoding="utf-8") as f:
    MAJORS = json.load(f)
SOURCE_FILE = find_data_file("academic_sources.json")
with SOURCE_FILE.open(encoding="utf-8") as f:
    ACADEMIC_SOURCES = json.load(f)

# Each item is stored in English for consistent database matching and translated for display.
SUBJECT_GROUPS = {
    "EMASI Subjects": [
        ("Mathematics", "Toán"), ("Literature", "Văn"), ("English", "Tiếng Anh"),
        ("Physics", "Lý"), ("Biology", "Sinh"), ("Chemistry", "Hoá học"),
        ("Music", "Âm nhạc"), ("Fine Arts", "Mỹ thuật"),
        ("ICT", "ICT"), ("Economics and Law", "Kinh tế pháp luật"),
        ("Technology", "Công nghệ"), ("Geography", "Địa lý"), ("History", "Lịch sử")
    ]
}

INTEREST_GROUPS = {
    "People, Mind & Learning": [
        ("Human behavior", "Hành vi con người"), ("Psychology", "Tâm lý học"),
        ("Cognitive processes", "Quá trình nhận thức"), ("Brain and neuroscience", "Não bộ và khoa học thần kinh"),
        ("Memory and attention", "Trí nhớ và sự chú ý"), ("Emotions and motivation", "Cảm xúc và động lực"),
        ("Mental health and wellbeing", "Sức khỏe tinh thần và hạnh phúc"),
        ("Education and learning", "Giáo dục và học tập"), ("Child and adolescent development", "Sự phát triển trẻ em và thanh thiếu niên"),
        ("Helping and supporting people", "Giúp đỡ và hỗ trợ mọi người"),
        ("Communication between people", "Giao tiếp giữa con người")
    ],
    "Society, Culture & Global Issues": [
        ("Social issues", "Các vấn đề xã hội"), ("Culture and society", "Văn hóa và xã hội"),
        ("History and civilizations", "Lịch sử và các nền văn minh"), ("Politics and public policy", "Chính trị và chính sách công"),
        ("Law and justice", "Pháp luật và công lý"), ("Human rights", "Nhân quyền"),
        ("International relations", "Quan hệ quốc tế"), ("Languages and cultures", "Ngôn ngữ và văn hóa"),
        ("Community development", "Phát triển cộng đồng"), ("Geography and places", "Địa lý và các vùng đất"),
        ("Cities and urban planning", "Thành phố và quy hoạch đô thị"), ("Travel and tourism", "Du lịch và khám phá")
    ],
    "Business, Economics & Leadership": [
        ("Economics and markets", "Kinh tế và thị trường"), ("Business and entrepreneurship", "Kinh doanh và khởi nghiệp"),
        ("Finance and investment", "Tài chính và đầu tư"), ("Marketing and branding", "Tiếp thị và xây dựng thương hiệu"),
        ("Leadership and management", "Lãnh đạo và quản lý"), ("Innovation and strategy", "Đổi mới và chiến lược"),
        ("Consumer behavior", "Hành vi người tiêu dùng"), ("Social enterprise", "Doanh nghiệp xã hội")
    ],
    "Technology, Data & Engineering": [
        ("Technology", "Công nghệ"), ("Artificial intelligence", "Trí tuệ nhân tạo"),
        ("Coding and software", "Lập trình và phần mềm"), ("Robotics and automation", "Robot và tự động hóa"),
        ("Data and patterns", "Dữ liệu và quy luật"), ("Cybersecurity", "An ninh mạng"),
        ("Digital products", "Sản phẩm số"), ("Engineering and invention", "Kỹ thuật và sáng chế"),
        ("Machines and systems", "Máy móc và hệ thống"), ("User experience design", "Thiết kế trải nghiệm người dùng")
    ],
    "Art, Design & Creative Expression": [
        ("Visual design and illustration", "Thiết kế thị giác và minh họa"), ("Fine art and painting", "Mỹ thuật và hội họa"),
        ("Creative expression", "Biểu đạt sáng tạo"), ("Music and sound", "Âm nhạc và âm thanh"),
        ("Performance and theatre", "Biểu diễn và sân khấu"), ("Dance and movement", "Múa và chuyển động"),
        ("Film and photography", "Điện ảnh và nhiếp ảnh"), ("Fashion and textiles", "Thời trang và dệt may"),
        ("Architecture and spaces", "Kiến trúc và không gian"), ("Craft and making things", "Thủ công và sáng tạo vật thể")
    ],
    "Nature, Environment & Living Systems": [
        ("Nature and wildlife", "Thiên nhiên và động vật hoang dã"), ("Environment and sustainability", "Môi trường và phát triển bền vững"),
        ("Climate change", "Biến đổi khí hậu"), ("Animals and living systems", "Động vật và hệ sinh thái"),
        ("Plants and agriculture", "Thực vật và nông nghiệp"), ("Oceans and marine life", "Đại dương và sinh vật biển"),
        ("Conservation", "Bảo tồn thiên nhiên"), ("Geography and earth processes", "Địa lý và các quá trình Trái Đất")
    ],
    "Science, Discovery & Problem Solving": [
        ("Scientific research", "Nghiên cứu khoa học"), ("Experiments and discovery", "Thí nghiệm và khám phá"),
        ("Mathematics and logic", "Toán học và tư duy logic"), ("Problem solving", "Giải quyết vấn đề"),
        ("Research and analysis", "Nghiên cứu và phân tích"), ("Space and astronomy", "Không gian và thiên văn học"),
        ("Health and human biology", "Sức khỏe và sinh học con người"), ("Ethics and big questions", "Đạo đức và những câu hỏi lớn"),
        ("Decision making", "Ra quyết định")
    ],
    "Communication, Media & Storytelling": [
        ("Storytelling and writing", "Kể chuyện và viết lách"), ("Language and communication", "Ngôn ngữ và giao tiếp"),
        ("Journalism and current affairs", "Báo chí và thời sự"), ("Film and media", "Điện ảnh và truyền thông"),
        ("Public speaking and debate", "Thuyết trình và tranh biện"), ("Content creation", "Sáng tạo nội dung"),
        ("Translation and interpretation", "Biên dịch và phiên dịch")
    ],
    "Health, Movement & Sport": [
        ("Sports and human movement", "Thể thao và vận động con người"), ("Fitness and performance", "Thể lực và thành tích"),
        ("Nutrition and food", "Dinh dưỡng và thực phẩm"), ("Public health", "Y tế công cộng"),
        ("Rehabilitation and wellbeing", "Phục hồi chức năng và sức khỏe")
    ]
}

T = {
    "English": {
        "nav":"Navigation", "home":"Home", "network":"My Exploration Network", "majors":"Explore Majors",
        "compare":"Compare Majors", "reflect":"Reflection", "about":"About This Website",
        "tagline":"Discover connections. Open new horizons.",
        "intro":"Explore how your interests and current school subjects may connect to academic disciplines, university majors and possible career areas.",
        "layers":"Connection layers", "sample":"Sample majors", "approach":"Approach",
        "steps":"Explore in five steps", "choose":"Choose", "connect":"Connect", "explore":"Explore",
        "compare_step":"Compare", "reflect_step":"Reflect",
        "choose_desc":"Select interests and current subjects.", "connect_desc":"Explore academic and career connections.",
        "explore_desc":"Learn about different majors.", "compare_desc":"Compare two or three majors.",
        "reflect_desc":"Plan your next questions and steps.",
        "notice":"This tool supports exploration. It does not measure ability, predict admission or decide which major is right for you.",
        "network_intro":"Choose interests and the subjects you are currently studying. The network shows possible links recorded in the sample database.",
        "why_connected":"Why are these connected?", "relationship":"Relationship type", "evidence_status":"Evidence status",
        "sample_notice":"Prototype note: these links come from the current sample database. They are illustrative mappings, not verified university prerequisites or evidence-backed recommendations.",
        "reset":"Reset view", "selected_node":"Selected node", "no_connections":"No direct connections are recorded for this node in the current sample data.",
        "click_hint":"Your selected interests and subjects are highlighted automatically. Click any node to inspect it and focus on its direct connections.",
        "major_intention":"Majors you are considering (up to 3)", "focus_view":"View one major at a time", "focus_view_help":"Choose a major to highlight its own pathway. Other selected majors remain visible but faded.", "undecided":"I have not decided yet (Undecided)", "major_intention_help":"Choose up to three majors from the same database used by the Network Map.",
        "interest":"Interests to explore", "subject":"EMASI subjects currently studied", "generate":"Generate my network",
        "fullmap":"1. Full connection map", "mapcaption":"Your selected interests and subjects are highlighted automatically, together with connected majors, disciplines and career areas. Other parts of the full map remain visible in grey.",
        "nodes":"2. Explore nodes", "node_prompt":"Choose a node to inspect", "direct":"Direct connections",
        "focus":"3. Focus on one connection", "related":"Related node", "candidates":"4. Majors to explore",
        "notranked":"These majors appear because some selected inputs overlap with sample database tags. They are not ranked or suitability recommendations.",
        "nomatch":"No direct connection is currently recorded in this sample database. You can still browse all majors.",
        "selectfirst":"Select at least one interest or current subject to generate a network.",
        "cluster":"Filter by academic area", "all":"All", "search_major":"Search majors", "related_subjects":"Related subjects",
        "disciplines":"Academic disciplines", "skills":"Relevant skills", "preparation":"Ways to prepare and explore", "careers":"Possible career areas",
        "choosemajors":"Choose two or three majors", "mainfocus":"Main focus", "mincompare":"Choose at least two majors to compare.",
        "areas":"Which majors would you like to explore further?", "questions":"What questions do you still have?",
        "next":"What will you investigate next?", "summary":"Create reflection summary", "ready":"Your reflection summary is ready.",
        "download":"Download summary", "about_title":"About Horizon", "about_sub":"A student-led space for thoughtful academic and career exploration.",
        "mission_title":"Our purpose", "mission":"Choosing a university major can feel complicated. Horizon helps students discover relationships between their interests, current school subjects, academic fields, university majors and possible career areas.",
        "how_title":"How to use the website", "how":"1. Select interests and current subjects. 2. Explore the connections shown in the network. 3. Read about majors and compare options. 4. Use the reflection page to record questions and possible next steps.",
        "principles_title":"What this tool does — and does not do",
        "principles":"Horizon is a starting point for exploration, not an assessment or an admissions tool. A connection does not mean a student is suited to a major, and the absence of a connection does not mean a major is unsuitable. Course requirements vary by university and country. Students should check official university information and talk with trusted teachers or advisors.",
        "database_title":"About the sample database", "database":"This prototype contains a limited set of example majors and mapped relationships. Some connections are illustrative and need further review against university curricula and reliable career information. The database will grow over time.",
        "feedback":"This is an evolving student project. Its content and translations may be refined through student feedback.",
        "language":"Language", "footer":"Explore with curiosity. Decide with information."
    },
    "Tiếng Việt": {
        "nav":"Điều hướng", "home":"Trang chủ", "network":"Mạng lưới khám phá của tôi", "majors":"Khám phá ngành học",
        "compare":"So sánh ngành học", "reflect":"Suy ngẫm", "about":"Giới thiệu trang web",
        "tagline":"Khám phá những kết nối. Mở ra những chân trời mới.",
        "intro":"Tìm hiểu cách sở thích và các môn học hiện tại có thể liên hệ với lĩnh vực học thuật, ngành học đại học và các nhóm nghề nghiệp tiềm năng.",
        "layers":"Các lớp kết nối", "sample":"Ngành học mẫu", "approach":"Cách tiếp cận",
        "steps":"Khám phá qua năm bước", "choose":"Lựa chọn", "connect":"Kết nối", "explore":"Tìm hiểu",
        "compare_step":"So sánh", "reflect_step":"Suy ngẫm",
        "choose_desc":"Chọn sở thích và các môn đang học.", "connect_desc":"Khám phá kết nối học thuật và nghề nghiệp.",
        "explore_desc":"Tìm hiểu các ngành học khác nhau.", "compare_desc":"So sánh hai hoặc ba ngành học.",
        "reflect_desc":"Lập kế hoạch cho câu hỏi và bước tiếp theo.",
        "notice":"Công cụ này hỗ trợ khám phá. Công cụ không đánh giá năng lực, dự đoán khả năng trúng tuyển hay quyết định ngành học phù hợp với bạn.",
        "network_intro":"Chọn sở thích và các môn bạn đang học. Mạng lưới sẽ hiển thị những kết nối có trong cơ sở dữ liệu mẫu.",
        "why_connected":"Vì sao có những kết nối này?", "relationship":"Loại mối liên hệ", "evidence_status":"Tình trạng bằng chứng",
        "sample_notice":"Lưu ý về phiên bản thử nghiệm: các kết nối này lấy từ cơ sở dữ liệu mẫu hiện tại. Đây là các mối liên hệ minh họa, không phải điều kiện đầu vào đại học đã được xác minh hay đề xuất phù hợp dựa trên bằng chứng.",
        "reset":"Đặt lại chế độ xem", "selected_node":"Nút đã chọn", "no_connections":"Dữ liệu mẫu hiện tại chưa ghi nhận kết nối trực tiếp cho nút này.",
        "click_hint":"Sở thích và môn học bạn chọn được làm nổi bật tự động. Nhấp vào bất kỳ nút nào để xem chi tiết và tập trung vào các kết nối trực tiếp.",
        "major_intention":"Các ngành học bạn đang cân nhắc (tối đa 3)", "focus_view":"Xem từng ngành học riêng biệt", "focus_view_help":"Chọn một ngành để làm nổi bật lộ trình riêng. Các ngành đã chọn khác vẫn hiển thị nhưng được làm mờ.", "undecided":"Tôi chưa xác định ngành học", "major_intention_help":"Chọn tối đa ba ngành từ cùng cơ sở dữ liệu được sử dụng trong Bản đồ kết nối.",
        "interest":"Sở thích muốn khám phá", "subject":"Các môn học hiện tại", "generate":"Tạo mạng lưới khám phá",
        "fullmap":"1. Bản đồ kết nối tổng thể", "mapcaption":"Sở thích và môn học bạn đã chọn sẽ được làm nổi bật tự động cùng với các ngành học, lĩnh vực học thuật và nhóm nghề nghiệp có liên quan. Những phần khác của bản đồ vẫn hiển thị mờ.",
        "nodes":"2. Khám phá các nút", "node_prompt":"Chọn một nút để xem chi tiết", "direct":"Các kết nối trực tiếp",
        "focus":"3. Tập trung vào một kết nối", "related":"Nút liên quan", "candidates":"4. Các ngành học có thể tìm hiểu",
        "notranked":"Các ngành xuất hiện vì một số lựa chọn của bạn trùng với nhãn trong cơ sở dữ liệu mẫu. Đây không phải bảng xếp hạng hay đề xuất mức độ phù hợp.",
        "nomatch":"Hiện chưa có kết nối trực tiếp được ghi nhận trong cơ sở dữ liệu mẫu này. Bạn vẫn có thể xem tất cả ngành học.",
        "selectfirst":"Hãy chọn ít nhất một sở thích hoặc môn học hiện tại để tạo mạng lưới.",
        "cluster":"Lọc theo lĩnh vực học thuật", "all":"Tất cả", "search_major":"Tìm kiếm ngành học", "related_subjects":"Các môn học liên quan",
        "disciplines":"Các lĩnh vực học thuật", "skills":"Kỹ năng liên quan", "preparation":"Cách chuẩn bị và khám phá", "careers":"Các nhóm nghề nghiệp có thể liên quan",
        "choosemajors":"Chọn hai hoặc ba ngành học", "mainfocus":"Trọng tâm chính", "mincompare":"Hãy chọn ít nhất hai ngành để so sánh.",
        "areas":"Bạn muốn tìm hiểu thêm những ngành nào?", "questions":"Bạn vẫn còn câu hỏi nào?",
        "next":"Bạn sẽ tìm hiểu điều gì tiếp theo?", "summary":"Tạo bản tóm tắt suy ngẫm", "ready":"Bản tóm tắt suy ngẫm đã sẵn sàng.",
        "download":"Tải bản tóm tắt", "about_title":"Giới thiệu Horizon", "about_sub":"Không gian khám phá học thuật và nghề nghiệp do học sinh chủ động định hướng.",
        "mission_title":"Mục đích của chúng tôi", "mission":"Việc lựa chọn ngành học đại học có thể khá phức tạp. Horizon giúp học sinh khám phá mối liên hệ giữa sở thích, các môn học hiện tại, lĩnh vực học thuật, ngành học đại học và các nhóm nghề nghiệp tiềm năng.",
        "how_title":"Cách sử dụng trang web", "how":"1. Chọn sở thích và các môn học hiện tại. 2. Khám phá những kết nối được thể hiện trong mạng lưới. 3. Đọc thông tin và so sánh các ngành học. 4. Sử dụng trang Suy ngẫm để ghi lại câu hỏi và những bước tiếp theo.",
        "principles_title":"Công cụ này làm gì — và không làm gì",
        "principles":"Horizon là điểm khởi đầu để khám phá, không phải bài kiểm tra năng lực hay công cụ tuyển sinh. Một kết nối không có nghĩa là học sinh chắc chắn phù hợp với ngành đó; việc không có kết nối cũng không có nghĩa là ngành đó không phù hợp. Chương trình học và yêu cầu đầu vào khác nhau tùy trường đại học và quốc gia. Học sinh nên kiểm tra thông tin chính thức của trường và trao đổi với giáo viên hoặc cố vấn đáng tin cậy.",
        "database_title":"Về cơ sở dữ liệu mẫu", "database":"Phiên bản thử nghiệm này có một số ngành học mẫu và các mối liên hệ được lập bản đồ. Một số kết nối chỉ mang tính minh họa và cần được kiểm tra thêm dựa trên chương trình đào tạo đại học và thông tin nghề nghiệp đáng tin cậy. Cơ sở dữ liệu sẽ tiếp tục được mở rộng.",
        "feedback":"Đây là dự án dành cho học sinh đang trong quá trình phát triển. Nội dung và bản dịch có thể được điều chỉnh dựa trên phản hồi của học sinh.",
        "language":"Ngôn ngữ", "footer":"Khám phá với sự tò mò. Lựa chọn dựa trên thông tin."
    }
}

def tr(key):
    return T[st.session_state.get("language", "English")][key]

def visible_label(en, vi):
    lang = st.session_state.get("language", "English")
    return en if lang == "English" else vi

def grouped_options(groups):
    result = []
    for group, items in groups.items():
        for en, vi in items:
            result.append((f"{group} · {en}" if st.session_state.language == "English"
                           else f"{group_vi(group)} · {vi}", en))
    return result

GROUP_VI = {
    "EMASI Subjects":"Các môn học tại EMASI",
    "Mathematics & Sciences":"Toán học và Khoa học",
    "Technology & Applied Sciences":"Công nghệ và Khoa học ứng dụng",
    "Humanities & Social Sciences":"Nhân văn và Khoa học xã hội",
    "Languages & Communication":"Ngôn ngữ và Truyền thông",
    "Arts & Creative Subjects":"Nghệ thuật và Sáng tạo",
    "Physical & Personal Development":"Thể chất và Phát triển cá nhân",
    "People, Mind & Learning":"Con người, Tâm trí và Học tập",
    "Society, Culture & Global Issues":"Xã hội, Văn hóa và Các vấn đề toàn cầu",
    "Business, Economics & Leadership":"Kinh doanh, Kinh tế và Lãnh đạo",
    "Technology, Data & Engineering":"Công nghệ, Dữ liệu và Kỹ thuật",
    "Art, Design & Creative Expression":"Nghệ thuật, Thiết kế và Sáng tạo",
    "Nature, Environment & Living Systems":"Thiên nhiên, Môi trường và Hệ sinh thái",
    "Science, Discovery & Problem Solving":"Khoa học, Khám phá và Giải quyết vấn đề",
    "Communication, Media & Storytelling":"Truyền thông, Báo chí và Kể chuyện",
    "Health, Movement & Sport":"Sức khỏe, Vận động và Thể thao"
}
def group_vi(name):
    return GROUP_VI.get(name, name)

SUBJECTS = [en for items in SUBJECT_GROUPS.values() for en, vi in items]
INTERESTS = sorted({en for items in INTEREST_GROUPS.values() for en, vi in items} |
                   {x for m in MAJORS.values() for x in m["interests"]})
SUBJECT_TRANSLATIONS = {en:vi for items in SUBJECT_GROUPS.values() for en,vi in items}
INTEREST_TRANSLATIONS = {en:vi for items in INTEREST_GROUPS.values() for en,vi in items}
DISCIPLINE_TRANSLATIONS = {en:vi for info in MAJORS.values() for en,vi in zip(info.get("disciplines", []), info.get("disciplines_vi", []))}
CAREER_TRANSLATIONS = {en:vi for info in MAJORS.values() for en,vi in zip(info.get("careers", []), info.get("careers_vi", []))}
for value in SUBJECTS:
    SUBJECT_TRANSLATIONS.setdefault(value, value)
for value in INTERESTS:
    INTEREST_TRANSLATIONS.setdefault(value, value)

st.markdown("""
<style>
:root { --ink:#17263D; --navy:#172B4D; --blue:#315B83; --cream:#F7F2EB; --sand:#E9D8C8; --teal:#6D9C98; }
.stApp {background:var(--cream); color:var(--ink);}
.block-container {max-width: 1280px; padding-top: 2rem; padding-bottom:3rem;}
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#172B4D,#223D59); }
section[data-testid="stSidebar"] * {color:#F7F2EB;}
.brand-mark {display:flex; align-items:center; gap:12px; padding:8px 2px 22px; color:#F7F2EB;}
.brand-mark .symbol {font-size:36px; line-height:1;}
.brand-mark .wordmark {font-family:Georgia,serif; font-size:23px; letter-spacing:.2px;}
.hero {padding:2.3rem; border-radius:18px; background:linear-gradient(120deg,#172B4D 0%,#315B83 65%,#6D8794 100%); color:white; box-shadow:0 10px 28px rgba(23,43,77,.13);}
.hero h1 {color:white; font-family:Georgia,serif; font-size:3.1rem; letter-spacing:-1px;}
.hero h3 {color:#F2E5D9; font-family:Georgia,serif; font-weight:400; font-style:italic;}
.hero p {color:#F8F5F0; max-width:850px; font-size:1.05rem;}
div[data-testid="stMetric"] {background:#EFE8DF;padding:14px;border-radius:12px;border:1px solid #E4D8CC;}
.stButton>button[kind="primary"], .stDownloadButton>button {background:#172B4D;color:white;border:1px solid #172B4D;border-radius:10px;}
div[data-testid="stExpander"] {background:rgba(255,255,255,.48); border-radius:12px;}
.small-note {font-size:0.9rem; opacity:0.85;}
</style>
""", unsafe_allow_html=True)

def node_id(kind, label):
    return f"{kind}::{label}"

def rank_exploration_areas(selected_interests, selected_subjects, selected_majors=None):
    """Rank exploration areas using interests as primary evidence and subjects as context."""
    selected_majors = selected_majors or []
    ranked = []
    for major, info in MAJORS.items():
        matched_interests = [x for x in selected_interests if x in info.get("interests", [])]
        verified_subjects = [c.get("subject_en") for c in info.get("emasi_subject_connections", [])
                             if c.get("verification_status") in ("Verified", "Supported")]
        matched_subjects = [x for x in selected_subjects if x in verified_subjects]
        if matched_interests or matched_subjects or major in selected_majors:
            # Explicitly considered majors are surfaced first as student intent,
            # not as an inferred suitability score.
            score = (10000 if major in selected_majors else 0) + 3 * len(matched_interests) + len(matched_subjects)
            ranked.append({"major": major, "score": score,
                           "matched_interests": matched_interests,
                           "matched_subjects": matched_subjects})
    ranked.sort(key=lambda x: (x["score"], len(x["matched_interests"]), len(x["matched_subjects"])), reverse=True)
    return ranked

def build_network(selected_interests, selected_subjects, selected_majors=None):
    """Build the complete academic map, then attach the student's selections."""
    selected_majors = selected_majors or []
    nodes, edges = {}, []
    def add_node(kind, label, description=""):
        key = node_id(kind, label)
        nodes[key] = {"id":key, "type":kind, "label":label, "description":description}
        return key
    def add_edge(source, target, relation, evidence):
        edge = {"source":source, "target":target, "relation":relation, "evidence":evidence}
        if edge not in edges:
            edges.append(edge)

    you = add_node("student", "Your exploration")
    for major in selected_majors:
        m = add_node("major", major, MAJORS[major]["overview"])
        add_edge(you, m, "considering", "Student-selected major intention")
    for interest in selected_interests:
        i = add_node("interest", interest, "An interest selected by the student.")
        add_edge(you, i, "interest in", "Student-selected input")
    for subject in selected_subjects:
        sub = add_node("subject", subject, "A current school subject selected by the student.")
        add_edge(you, sub, "currently studies", "Student-selected input")

    # All majors, disciplines and career areas are always present in Full Map.
    for major, info in MAJORS.items():
        m = add_node("major", major, info["overview"])
        for discipline in info["disciplines"]:
            d = add_node("discipline", discipline, "An academic discipline connected to this major in the sample database.")
            add_edge(m, d, "draws on", "Major database: academic disciplines")
        for career in info["careers"]:
            c = add_node("career", career, "A possible related career area; not a guaranteed outcome.")
            add_edge(m, c, "may connect to", "Major database: potential career areas")

    # Student inputs connect to majors only where the prototype's explicit
    # interest/subject mapping supports a relationship.
    candidates = set(selected_majors)
    for major, info in MAJORS.items():
        mkey = node_id("major", major)
        for interest in selected_interests:
            if interest in info["interests"]:
                add_edge(node_id("interest", interest), mkey, "interest connection", "Major database: interests")
                candidates.add(major)
        for connection in info.get("emasi_subject_connections", []):
            subject = connection.get("subject_en")
            if subject in selected_subjects and connection.get("verification_status") in ("Verified", "Supported"):
                evidence_label = connection.get("source_title", "Claim-level source record")
                add_edge(node_id("subject", subject), mkey, connection.get("relationship_type", "academic connection"), evidence_label)
                candidates.add(major)
    return nodes, edges, sorted(candidates)


def graphviz_source(nodes, edges):
    colors = {"student":"#DCEBFA","interest":"#E8E3FA","subject":"#E2F2E8",
              "major":"#FFF0D9","discipline":"#FCE4E4","career":"#E8EEF8"}
    lines = ["digraph G {",'rankdir="LR";',
        'graph [bgcolor="transparent", nodesep="0.35", ranksep="0.75", pad="0.2"];',
        'node [shape=box, style="rounded,filled", fontname="Arial", fontsize=10, color="#93A4B7", margin="0.13,0.09"];',
        'edge [fontname="Arial", fontsize=8, color="#8393A6", arrowsize="0.65"];']
    for key,n in nodes.items():
        label = n["label"].replace('"', "'")
        lines.append(f'"{key}" [label="{label}", fillcolor="{colors.get(n["type"],"#FFFFFF")}"];')
    for e in edges:
        lines.append(f'"{e["source"]}" -> "{e["target"]}" [label="{e["relation"]}"];')
    lines.append("}")
    return "\n".join(lines)

def node_options(nodes):
    order = ["student","interest","subject","major","discipline","career"]
    return [(f'{n["type"].title()} · {n["label"]}', key) for kind in order
            for key,n in nodes.items() if n["type"] == kind]


MAJOR_TRANSLATIONS = {
    "Cognitive Science":"Khoa học nhận thức", "Psychology":"Tâm lý học", "Computer Science":"Khoa học máy tính", "Data Science":"Khoa học dữ liệu", "Economics":"Kinh tế học", "Biology":"Sinh học", "Mechanical Engineering":"Kỹ thuật cơ khí", "Finance":"Tài chính", "Chemistry":"Hóa học", "Physics":"Vật lý", "Environmental Science":"Khoa học môi trường", "Architecture":"Kiến trúc", "Electrical Engineering":"Kỹ thuật điện", "Civil Engineering":"Kỹ thuật xây dựng", "Political Science":"Khoa học chính trị", "Sociology":"Xã hội học", "Linguistics":"Ngôn ngữ học", "Education":"Giáo dục học", "Accounting":"Kế toán", "Communication & Media Studies":"Truyền thông và nghiên cứu truyền thông"
}

NODE_TYPE_VI = {
    "student":"Khám phá của bạn", "interest":"Sở thích", "subject":"Các môn học hiện có tại EMASI",
    "major":"Ngành học đại học", "discipline":"Lĩnh vực học thuật", "career":"Lĩnh vực nghề nghiệp"
}
RELATION_VI = {
    "interest in":"quan tâm đến", "currently studies":"đang học", "considering":"đang cân nhắc",
    "interest connection":"kết nối sở thích", "academic subject connection":"kết nối môn học",
    "draws on":"có nền tảng từ", "may connect to":"có thể liên quan đến"
}

def translated_node_label(node):
    label = node["label"]
    if st.session_state.language == "Tiếng Việt":
        label = MAJOR_TRANSLATIONS.get(label, SUBJECT_TRANSLATIONS.get(label, INTEREST_TRANSLATIONS.get(label, DISCIPLINE_TRANSLATIONS.get(label, CAREER_TRANSLATIONS.get(label, label)))))
        return f'{NODE_TYPE_VI.get(node["type"], node["type"])}: {label}'
    return f'{node["type"].title()}: {label}'

def make_interactive_graph(nodes, edges, selected_key=None, focus_keys=None):
    # Default state: focus on the student's selected interests and current
    # subjects, then illuminate their connected majors and the majors'
    # academic-discipline / career branches. Keep the wider map visible but dim.
    adjacent = set()
    if selected_key:
        adjacent.add(selected_key)
        for edge in edges:
            if edge["source"] == selected_key:
                adjacent.add(edge["target"])
            elif edge["target"] == selected_key:
                adjacent.add(edge["source"])
    else:
        # focus_keys are the curated nodes of the strongest-supported
        # academic exploration cluster, not every reachable node.
        adjacent.update(focus_keys or [])

    palette = {
        "student":"#315B83", "interest":"#8D7DB8", "subject":"#6D9C98",
        "major":"#C18B4A", "discipline":"#B87575", "career":"#7187A6"
    }
    graph_nodes = []
    for key, item in nodes.items():
        active = key in adjacent if (selected_key or focus_keys) else True
        color = palette.get(item["type"], "#8393A6") if active else "#D9DEE5"
        border = "#172B4D" if key == selected_key else "#FFFFFF"
        size = 31 if key == selected_key else (23 if active else 17)
        display_label = item["label"]
        if st.session_state.language == "Tiếng Việt":
            display_label = MAJOR_TRANSLATIONS.get(display_label, SUBJECT_TRANSLATIONS.get(display_label, INTEREST_TRANSLATIONS.get(display_label, DISCIPLINE_TRANSLATIONS.get(display_label, CAREER_TRANSLATIONS.get(display_label, display_label)))))
        graph_nodes.append(Node(
            id=key, label=display_label, title=(MAJORS.get(item["label"], {}).get("overview_vi", item["description"]) if st.session_state.language == "Tiếng Việt" and item["type"] == "major" else display_label),
            size=size,
            color={"background":color, "border":border, "highlight":{"background":color,"border":"#172B4D"}},
            borderWidth=3 if key == selected_key else 1,
            font={"color":"#17263D" if active else "#A6AFBA", "size":15 if active else 12}
        ))

    graph_edges = []
    for edge in edges:
        if selected_key:
            active = selected_key in (edge["source"], edge["target"])
        elif focus_keys:
            active = edge["source"] in adjacent and edge["target"] in adjacent
        else:
            active = True
        graph_edges.append(Edge(
            source=edge["source"], target=edge["target"], label=(RELATION_VI.get(edge["relation"], edge["relation"]) if st.session_state.language == "Tiếng Việt" else edge["relation"]),
            color="#315B83" if active else "#E1E5EA",
            width=3 if (selected_key or focus_keys) and active else 1.2,
            font={"color":"#52657B" if active else "#C1C8D1", "size":10},
            arrows="to"
        ))

    config = Config(
        width="100%", height=650, directed=True, physics=True, hierarchical=False,
        nodeHighlightBehavior=False, collapsible=False,
        interaction={"hover":True, "navigationButtons":True, "keyboard":True},
        physics_options={"solver":"forceAtlas2Based",
                         "forceAtlas2Based":{"gravitationalConstant":-45,"springLength":150,"springConstant":0.08}}
    )
    return agraph(nodes=graph_nodes, edges=graph_edges, config=config)

with st.sidebar:
    st.image(str(Path(__file__).parent / 'horizon_logo.svg'), use_container_width=True)
    lang = st.selectbox("Language / Ngôn ngữ", ["English","Tiếng Việt"],
                        index=0 if st.session_state.get("language","English")=="English" else 1)
    st.session_state.language = lang
    pages = [tr("home"),tr("network"),tr("majors"),tr("compare"),tr("reflect"),tr("about")]
    page = st.radio(tr("nav"), pages)
    st.divider()
    st.caption(tr("footer"))

if page == tr("home"):
    st.markdown(f"""<div class="hero"><div style="font-size:2.3rem; margin-bottom:.4rem;">⌒✦</div><h1>Horizon</h1><h3>{tr("tagline")}</h3><p>{tr("intro")}</p></div>""", unsafe_allow_html=True)
    st.write("")
    features = {
      "English":[("Student-centered","You explore and decide at your own pace."),("Connection-based","See how interests, subjects and majors relate."),("Exploratory, not decisive","Reflect, compare and consider possible directions."),("Bilingual support","Available in English and Vietnamese.")],
      "Tiếng Việt":[("Lấy học sinh làm trung tâm","Bạn tự khám phá và đưa ra lựa chọn theo nhịp độ của mình."),("Dựa trên các mối liên hệ","Tìm hiểu cách sở thích, môn học và ngành học kết nối với nhau."),("Khuyến khích khám phá","Suy ngẫm, so sánh và cân nhắc nhiều hướng đi."),("Hỗ trợ song ngữ","Có thể sử dụng bằng tiếng Anh và tiếng Việt.")]
    }
    feature_cols=st.columns(4)
    for col,(heading,body) in zip(feature_cols,features[st.session_state.language]):
        with col:
            st.markdown(f"### {heading}")
            st.caption(body)
    st.divider()
    st.subheader(tr("steps"))
    cols = st.columns(5)
    step_icons=["✧","▤","⌘","⚖","✎"]
    for col,icon,title,desc in zip(cols,step_icons,[tr("choose"),tr("connect"),tr("explore"),tr("compare_step"),tr("reflect_step")],
        [tr("choose_desc"),tr("connect_desc"),tr("explore_desc"),tr("compare_desc"),tr("reflect_desc")]):
        with col:
            st.markdown(f"### {icon}")
            st.markdown(f"**{title}**")
            st.caption(desc)
    st.divider()
    st.subheader("About Horizon" if st.session_state.language=="English" else "Giới thiệu Horizon")
    st.write(tr("mission"))
    st.info(tr("notice"))

elif page == tr("network"):
    st.title(tr("network"))
    st.write(tr("network_intro"))
    interest_pairs = grouped_options(INTEREST_GROUPS)
    subject_pairs = grouped_options(SUBJECT_GROUPS)
    interest_label_to_key = {label:key for label,key in interest_pairs}
    subject_label_to_key = {label:key for label,key in subject_pairs}
    # The major selector is generated directly from the Network Map database.
    # Keys remain canonical English IDs in both languages; only labels change.
    major_label_to_key = {
        (f"{major} · {info.get('name_vi', major)}" if st.session_state.language == "Tiếng Việt" else major): major
        for major, info in MAJORS.items()
    }
    with st.form("network_inputs"):
        chosen_major_labels = st.multiselect(
            tr("major_intention"), list(major_label_to_key), max_selections=3,
            help=tr("major_intention_help"))
        undecided = st.checkbox(tr("undecided"), value=False)
        chosen_interest_labels = st.multiselect(tr("interest"), list(interest_label_to_key))
        chosen_subject_labels = st.multiselect(tr("subject"), list(subject_label_to_key))
        submitted = st.form_submit_button(tr("generate"), type="primary")
    if submitted:
        st.session_state.chosen_majors = [] if undecided else [major_label_to_key[x] for x in chosen_major_labels]
        st.session_state.undecided_major = undecided
        st.session_state.chosen_interests = [interest_label_to_key[x] for x in chosen_interest_labels]
        st.session_state.chosen_subjects = [subject_label_to_key[x] for x in chosen_subject_labels]
        st.session_state.network_generated = True
        st.session_state.selected_network_node = None

    if st.session_state.get("network_generated"):
        interests = st.session_state.get("chosen_interests",[])
        subjects = st.session_state.get("chosen_subjects",[])
        intended_majors = st.session_state.get("chosen_majors",[])
        if not interests and not subjects and not intended_majors:
            st.warning(tr("selectfirst"))
        else:
            nodes, edges, candidates = build_network(interests, subjects, intended_majors)
            st.subheader(tr("fullmap"))
            st.caption(
                "This is the complete map. Your selected interests and current subjects illuminate the matching academic area; all other areas remain visible but faded."
                if st.session_state.language == "English" else
                "Đây là bản đồ đầy đủ. Sở thích và môn học hiện tại bạn đã chọn sẽ làm nổi bật khu vực học thuật phù hợp; các khu vực khác vẫn hiển thị nhưng được làm mờ."
            )
            st.caption(
                "Click a node to inspect its direct connections. If you selected multiple majors, use the focus selector to inspect each pathway separately; other selected majors remain visible but faded."
                if st.session_state.language == "English" else
                "Nhấp vào một nút để xem các kết nối trực tiếp. Nếu bạn chọn nhiều ngành, hãy dùng bộ chọn trọng tâm để xem riêng từng lộ trình; các ngành đã chọn khác vẫn hiển thị nhưng được làm mờ."
            )
            st.info(tr("sample_notice"))
            if not candidates:
                st.warning(
                    "No direct matches were found in the current sample database. Your selections are still shown; the map does not infer a connection without a database relationship."
                    if st.session_state.language == "English" else
                    "Không tìm thấy mối liên hệ trực tiếp trong cơ sở dữ liệu mẫu hiện tại. Các lựa chọn của bạn vẫn được hiển thị; bản đồ không tự suy đoán mối liên hệ khi chưa có dữ liệu hỗ trợ."
                )

            selected_key = st.session_state.get("selected_network_node")
            if selected_key not in nodes:
                selected_key = None

            # Find the strongest-supported exploration cluster. Interests are
            # the primary signal; current school subjects provide context.
            ranked_areas = rank_exploration_areas(interests, subjects, intended_majors)
            focus_keys = []
            primary_area = ranked_areas[0] if ranked_areas else None
            if intended_majors:
                # Keep the complete map available, but illuminate one selected
                # major pathway at a time to avoid three dense clusters merging
                # into a single visual mass. The selector is navigation only;
                # it does not change the student's stated major choices.
                focus_options = intended_majors
                focus_labels = {
                    m: (m if st.session_state.language == "English" else MAJOR_TRANSLATIONS.get(m, m))
                    for m in focus_options
                }
                active_focus_major = st.selectbox(
                    tr("focus_view"), focus_options,
                    format_func=lambda m: focus_labels[m],
                    help=tr("focus_view_help"),
                    key="v25_active_focus_major"
                )
                focus_keys.append(node_id("major", active_focus_major))
                focus_keys.extend(node_id("discipline", d) for d in MAJORS[active_focus_major].get("disciplines", []))
                focus_keys.extend(node_id("career", c) for c in MAJORS[active_focus_major].get("careers", []))
                focus_keys.extend(node_id("interest", x) for x in interests if x in MAJORS[active_focus_major].get("interests", []))
                focus_keys.extend(node_id("subject", x) for x in subjects if x in [c.get("subject_en") for c in MAJORS[active_focus_major].get("emasi_subject_connections", []) if c.get("verification_status") in ("Verified", "Supported")])
            elif primary_area:
                major = primary_area["major"]
                focus_keys.append(node_id("major", major))
                focus_keys.extend(node_id("discipline", d) for d in MAJORS[major].get("disciplines", []))
                focus_keys.extend(node_id("career", c) for c in MAJORS[major].get("careers", []))
                focus_keys.extend(node_id("interest", x) for x in primary_area["matched_interests"])
                focus_keys.extend(node_id("subject", x) for x in primary_area["matched_subjects"])
                # Preserve equally strong areas as distinct highlighted clusters.
                for area in ranked_areas[1:]:
                    if area["score"] == primary_area["score"]:
                        other = area["major"]
                        focus_keys.append(node_id("major", other))
                        focus_keys.extend(node_id("discipline", d) for d in MAJORS[other].get("disciplines", []))
                        focus_keys.extend(node_id("career", c) for c in MAJORS[other].get("careers", []))
                        focus_keys.extend(node_id("interest", x) for x in area["matched_interests"])
                        focus_keys.extend(node_id("subject", x) for x in area["matched_subjects"])
            else:
                # No interest-to-major evidence: do not infer a major from
                # school subjects alone.
                focus_keys = [node_id("interest", x) for x in interests]
            if intended_majors:
                labels = intended_majors if st.session_state.language == "English" else [MAJORS[m].get("name_vi", m) for m in intended_majors]
                st.success(("Primary exploration focus from your stated intention: " + ", ".join(labels) + ". Related links are shown separately; this is not a suitability assessment.") if st.session_state.language == "English" else ("Trọng tâm khám phá theo lựa chọn của bạn: " + ", ".join(labels) + ". Các mối liên hệ khác được hiển thị riêng; đây không phải đánh giá mức độ phù hợp."))
            elif primary_area:
                area_name = primary_area["major"]
                area_display = area_name if st.session_state.language == "English" else MAJOR_TRANSLATIONS.get(area_name, area_name)
                st.success(
                    f"Highlighted exploration area: {area_display}. This is a navigation focus, not a suitability assessment."
                    if st.session_state.language == "English" else
                    f"Khu vực khám phá được làm nổi bật: {area_display}. Đây là trọng tâm hiển thị, không phải đánh giá mức độ phù hợp."
                )
            clicked = make_interactive_graph(nodes, edges, selected_key, focus_keys=focus_keys)
            if clicked and clicked in nodes and clicked != selected_key:
                st.session_state.selected_network_node = clicked
                st.rerun()

            selected_key = st.session_state.get("selected_network_node")
            if selected_key in nodes:
                selected_node = nodes[selected_key]
                st.divider()
                st.subheader(tr("selected_node"))
                st.markdown(f"### {translated_node_label(selected_node)}")
                st.write((MAJORS.get(selected_node["label"], {}).get("overview_vi", selected_node["description"]) if st.session_state.language == "Tiếng Việt" else selected_node["description"]))

                connected_edges = [e for e in edges if selected_key in (e["source"], e["target"])]
                if connected_edges:
                    st.subheader(tr("direct"))
                    for edge in connected_edges:
                        other_key = edge["target"] if edge["source"] == selected_key else edge["source"]
                        other_node = nodes[other_key]
                        relation = edge["relation"]
                        if st.session_state.language == "Tiếng Việt":
                            relation = RELATION_VI.get(relation, relation)
                        with st.expander(f'{translated_node_label(other_node)} · {relation}'):
                            st.markdown(f"**{tr('why_connected')}**")
                            if edge["relation"] == "interest connection":
                                explanation = ("This link is based on an interest tag in the sample major database."
                                               if st.session_state.language == "English" else
                                               "Mối liên hệ này dựa trên nhãn sở thích trong cơ sở dữ liệu ngành học mẫu.")
                            elif edge["relation"] == "academic subject connection":
                                explanation = ("This link is based on a related-subject tag in the sample major database; it is not necessarily an admission prerequisite."
                                               if st.session_state.language == "English" else
                                               "Mối liên hệ này dựa trên nhãn môn học liên quan trong cơ sở dữ liệu mẫu; không nhất thiết là điều kiện đầu vào.")
                            elif edge["relation"] == "draws on":
                                explanation = ("This is an academic-discipline tag associated with the sample major entry."
                                               if st.session_state.language == "English" else
                                               "Đây là nhãn lĩnh vực học thuật được gắn với ngành học mẫu.")
                            elif edge["relation"] == "may connect to":
                                explanation = ("This is an illustrative possible career-area association, not a guaranteed career outcome."
                                               if st.session_state.language == "English" else
                                               "Đây là mối liên hệ minh họa với lĩnh vực nghề nghiệp có thể liên quan, không phải kết quả nghề nghiệp được đảm bảo.")
                            else:
                                explanation = edge["evidence"]
                            st.write(explanation)
                            st.caption(f'{tr("relationship")}: {relation}')
                            st.caption(f'{tr("evidence_status")}: Sample database tag — source verification pending.')
                else:
                    st.info(tr("no_connections"))

                if st.button(tr("reset"), key="reset_network_view"):
                    st.session_state.selected_network_node = None
                    st.rerun()

            st.subheader(tr("candidates"))
            if candidates:
                candidate_display = [f"{m} (your stated choice)" if m in intended_majors and st.session_state.language == "English" else (f"{MAJORS[m].get('name_vi',m)} (lựa chọn của bạn)" if m in intended_majors else (m if st.session_state.language == "English" else MAJORS[m].get("name_vi",m))) for m in candidates]
                st.write(", ".join(candidate_display))
                st.caption(tr("notranked"))
            else:
                st.info(tr("nomatch"))

elif page == tr("majors"):
    st.title(tr("majors"))
    q = st.text_input(tr("search_major"), placeholder="e.g. Psychology / Tâm lý học")
    clusters = sorted({v["cluster"] for v in MAJORS.values()})
    cluster_labels = {tr("all"): None}
    for c in clusters:
        cluster_labels[next((v.get("cluster_vi",c) for v in MAJORS.values() if v["cluster"] == c),c) if st.session_state.language == "Tiếng Việt" else c] = c
    chosen_cluster = st.selectbox(tr("cluster"), list(cluster_labels))
    for name,info in MAJORS.items():
        shown_name = info.get("name_vi", name) if st.session_state.language == "Tiếng Việt" else name
        shown_cluster = info.get("cluster_vi", info["cluster"]) if st.session_state.language == "Tiếng Việt" else info["cluster"]
        if cluster_labels[chosen_cluster] and info["cluster"] != cluster_labels[chosen_cluster]: continue
        if q and q.casefold() not in name.casefold() and q.casefold() not in shown_name.casefold(): continue
        with st.expander(f"{shown_name} · {shown_cluster}"):
            st.write(info.get("overview_vi",info["overview"]) if st.session_state.language == "Tiếng Việt" else info["overview"])
            a,b = st.columns(2)
            with a:
                st.markdown(f"**{tr('disciplines')}**"); st.write(", ".join(info.get("disciplines_vi", info["disciplines"])) if st.session_state.language == "Tiếng Việt" else ", ".join(info["disciplines"]))
                st.caption("Academic disciplines are university-level fields of study; they are not the same thing as EMASI school subjects." if st.session_state.language == "English" else "Các lĩnh vực học thuật là lĩnh vực nghiên cứu ở bậc đại học; chúng không đồng nghĩa với các môn học tại EMASI.")
            with b:
                st.markdown(f"**{tr('skills')}**"); st.write(", ".join(info.get("skills_vi",info["skills"])) if st.session_state.language == "Tiếng Việt" else ", ".join(info["skills"]))
                st.markdown(f"**{tr('careers')}**"); st.write(", ".join(info.get("careers_vi", info["careers"])) if st.session_state.language == "Tiếng Việt" else ", ".join(info["careers"]))
            st.markdown(f"**{tr('preparation')}**")
            prep = info.get("preparation_vi",info["preparation"]) if st.session_state.language == "Tiếng Việt" else info["preparation"]
            for item in prep: st.markdown(f"- {item}")
            st.caption(info.get("caveat_vi",info["caveat"]) if st.session_state.language == "Tiếng Việt" else info["caveat"])

            # Expanded academic profile; these fields are descriptive, not admission requirements.
            detail_fields = [
                ("academic_foundations", "Academic foundations" if st.session_state.language == "English" else "Nền tảng học thuật"),
                ("related_disciplines", "Related disciplines" if st.session_state.language == "English" else "Các lĩnh vực liên quan"),
                ("specialized_applications", "Specialized applications" if st.session_state.language == "English" else "Ứng dụng chuyên sâu"),
                ("research_areas", "Research directions" if st.session_state.language == "English" else "Hướng nghiên cứu"),
                ("limitations", "Scope and limitations to note" if st.session_state.language == "English" else "Phạm vi và giới hạn cần lưu ý")
            ]
            for field, label in detail_fields:
                field_vi = field + "_vi"
                values = info.get(field, []) if st.session_state.language == "English" else info.get(field_vi, info.get(field, []))
                if values:
                    st.markdown(f"**{label}**")
                    for value in values:
                        st.markdown(f"- {value}")
            note_key = "taxonomy_note_vi" if st.session_state.language == "Tiếng Việt" else "taxonomy_note"
            if info.get(note_key): st.caption(info[note_key])

            # Subject guidance answers the student's practical question: which EMASI subjects
            # are useful to explore for this major? It is deliberately separate from verified
            # institution-specific prerequisite/connection claims.
            st.markdown("### EMASI subjects to consider" if st.session_state.language == "English" else "### Các môn EMASI nên cân nhắc")
            st.caption(info.get("subject_guidance_note_en", "") if st.session_state.language == "English" else info.get("subject_guidance_note_vi", ""))
            audit = info.get("evidence_audit_summary", {})
            audit_status = audit.get("status_en", "") if st.session_state.language == "English" else audit.get("status_vi", "")
            audit_note = audit.get("note_en", "") if st.session_state.language == "English" else audit.get("note_vi", "")
            if audit_status:
                st.info(f"**{audit_status}**\\n\\n{audit_note}")
            guidance = info.get("emasi_subject_guidance", [])
            if guidance:
                sourced_guidance = sum(1 for item in guidance if item.get("evidence_refs"))
                unsourced_guidance = len(guidance) - sourced_guidance
                if st.session_state.language == "English":
                    st.caption(f"Evidence coverage for this major: {sourced_guidance}/{len(guidance)} subject suggestions have attached curriculum references; {unsourced_guidance} still need claim-level sources. References support university-level context and do not verify EMASI syllabus alignment or admission prerequisites.")
                else:
                    st.caption(f"Mức độ bao phủ bằng chứng cho ngành này: {sourced_guidance}/{len(guidance)} gợi ý môn học có nguồn chương trình đại học đính kèm; {unsourced_guidance} gợi ý vẫn cần nguồn ở cấp độ nhận định. Các nguồn chỉ hỗ trợ bối cảnh chương trình đại học, không xác minh sự tương ứng với đề cương EMASI hoặc điều kiện tuyển sinh.")
                role_order = ["Strong preparation", "Helpful support", "Pathway-dependent", "Application-dependent"]
                for role in role_order:
                    items = [g for g in guidance if g.get("role_en") == role]
                    if not items:
                        continue
                    role_label = items[0].get("role_en") if st.session_state.language == "English" else items[0].get("role_vi")
                    st.markdown(f"**{role_label}**")
                    for item in items:
                        subject_name = item.get("subject_en") if st.session_state.language == "English" else item.get("subject_vi")
                        reason = item.get("why_en") if st.session_state.language == "English" else item.get("why_vi")
                        st.markdown(f"- **{subject_name}** — {reason}")
                        # Expanded bilingual explanation: what to focus on and why it matters.
                        detail = item.get("focus_en", "") if st.session_state.language == "English" else item.get("focus_vi", "")
                        evidence_text = item.get("evidence_en", "") if st.session_state.language == "English" else item.get("evidence_vi", "")
                        if detail:
                            st.markdown(("  - **What to focus on:** " if st.session_state.language == "English" else "  - **Nội dung nên chú ý:** ") + detail)
                        if evidence_text:
                            st.markdown(("  - **Academic basis:** " if st.session_state.language == "English" else "  - **Cơ sở học thuật:** ") + evidence_text)
                        # Claim-level evidence traceability. Sources are shown with their actual scope;
                        # a major-level source is never presented as proof of an EMASI prerequisite.
                        claim_id = item.get("claim_id", "")
                        status = item.get("evidence_status_en", "") if st.session_state.language == "English" else item.get("evidence_status_vi", "")
                        if status:
                            st.caption(("Evidence status: " if st.session_state.language == "English" else "Trạng thái bằng chứng: ") + status)
                        scope = item.get("evidence_scope_en", "") if st.session_state.language == "English" else item.get("evidence_scope_vi", "")
                        if scope:
                            st.caption(scope)
                        refs = item.get("evidence_refs", [])
                        if refs:
                            st.markdown(("**Curriculum / disciplinary references**" if st.session_state.language == "English" else "**Nguồn tham khảo chương trình / ngành học**"))
                            for ref in refs:
                                st.markdown(f"- [{ref.get('institution', 'Institution')}: {ref.get('title', 'Reference')}]({ref.get('url', '#')})")
                                ref_scope = ref.get("scope_en", "") if st.session_state.language == "English" else ref.get("scope_vi", "")
                                if ref_scope:
                                    st.caption(ref_scope)
                        else:
                            st.caption("No claim-level curriculum source is attached to this subject mapping yet." if st.session_state.language == "English" else "Hiện chưa có nguồn chương trình học ở cấp độ nhận định được gắn với mối liên hệ môn học này.")
            if st.session_state.language == "English":
                st.info(info.get("selection_help_en", "Start with the core subjects, then consider supporting subjects based on your interests."))
            else:
                st.info(info.get("selection_help_vi", "Hãy bắt đầu với các môn nền tảng, sau đó cân nhắc môn hỗ trợ theo sở thích của bạn."))
            pathway_note = info.get("pathway_choice_en" if st.session_state.language == "English" else "pathway_choice_vi")
            if pathway_note:
                st.markdown("**How to choose when the major has several pathways**" if st.session_state.language == "English" else "**Cách chọn môn khi ngành có nhiều hướng chuyên sâu**")
                st.write(pathway_note)
            st.caption("These are subject-exploration suggestions, not compulsory subjects or admission requirements. University requirements differ by programme." if st.session_state.language == "English" else "Đây là gợi ý môn học để khám phá, không phải môn bắt buộc hay điều kiện tuyển sinh. Yêu cầu khác nhau tùy chương trình đại học.")

            st.markdown("**Verified programme-specific subject connections**" if st.session_state.language == "English" else "**Kết nối môn học đã được xác minh theo từng chương trình đại học**")
            connections = [c for c in info.get("emasi_subject_connections", []) if c.get("verification_status") in ("Verified", "Supported")]
            if connections:
                for c in connections:
                    subject_name = c.get("subject_en", "") if st.session_state.language == "English" else c.get("subject_vi", c.get("subject_en", ""))
                    explanation = c.get("evidence_explanation_en", c.get("evidence_explanation", "")) if st.session_state.language == "English" else c.get("evidence_explanation_vi", c.get("evidence_explanation", ""))
                    st.markdown(f"- **{subject_name}** — {c.get('relationship_type','')}: {explanation}")
                    if c.get("source_url"):
                        st.markdown(f"  - [Source: {c.get('source_title','Official source')}]({c['source_url']})")
            else:
                st.info("No programme-specific EMASI subject link has been verified yet. The guidance above is exploratory; it is not presented as a confirmed university prerequisite." if st.session_state.language == "English" else "Hiện chưa có kết nối môn học EMASI nào được xác minh theo chương trình đại học cụ thể. Các gợi ý phía trên chỉ phục vụ khám phá, không được xem là điều kiện đầu vào đã xác nhận.")

            # Major-specific reference links (bilingual; scope is stated to avoid overclaiming).
            profile_refs = info.get("profile_reference_links", [])
            if profile_refs:
                st.markdown("**References for this major**" if st.session_state.language == "English" else "**Nguồn tham khảo cho ngành này**")
                ref_note = info.get("profile_reference_note_en", "") if st.session_state.language == "English" else info.get("profile_reference_note_vi", "")
                st.caption(ref_note)
                for ref in profile_refs:
                    st.markdown(f"- **{ref.get('institution', 'Reference organisation')}** — [{ref.get('title', 'Academic reference')}]({ref.get('url', '#')})")
                    ref_use = ref.get("use_en", "") if st.session_state.language == "English" else ref.get("use_vi", "")
                    if ref_use:
                        st.caption(ref_use)

            # Academic Evidence & Sources: only explicitly reviewed claims carry verified status.
            evidence = ACADEMIC_SOURCES.get(name)
            st.divider()
            st.markdown("### Academic Evidence & Sources" if st.session_state.language == "English" else "### Bằng chứng học thuật & Nguồn")
            if evidence:
                status = evidence.get("status_vi", evidence["status"]) if st.session_state.language == "Tiếng Việt" else evidence["status"]
                st.caption(("Evidence status: " if st.session_state.language == "English" else "Trạng thái bằng chứng: ") + status)
                scope = evidence.get("scope_vi", evidence["scope"]) if st.session_state.language == "Tiếng Việt" else evidence["scope"]
                st.write(scope)
                for claim in evidence.get("claims", []):
                    claim_text = claim.get("claim_vi", claim["claim"]) if st.session_state.language == "Tiếng Việt" else claim["claim"]
                    claim_type = claim.get("type_vi", claim["type"]) if st.session_state.language == "Tiếng Việt" else claim["type"]
                    claim_status = claim.get("status_vi", claim["status"]) if st.session_state.language == "Tiếng Việt" else claim["status"]
                    with st.expander(claim_text):
                        st.caption(("Evidence category: " if st.session_state.language == "English" else "Loại bằng chứng: ") + claim_type)
                        st.caption(("Verification: " if st.session_state.language == "English" else "Xác minh: ") + claim_status)
                        for source in claim.get("sources", []):
                            st.markdown(f"- **{source['institution']}** — [{source['title']}]({source['url']})")
                            st.caption(source.get("source_type", "") if st.session_state.language == "English" else source.get("source_type_vi", source.get("source_type", "")))
                            if source.get("listed_programme_name"):
                                label = "Programme name listed by university: " if st.session_state.language == "English" else "Tên chương trình theo danh mục của trường: "
                                st.caption(label + source["listed_programme_name"])
            else:
                st.caption("Evidence status: Pending source audit." if st.session_state.language == "English" else "Trạng thái bằng chứng: Chờ kiểm tra nguồn.")
                st.write(
                    "The academic profile is currently an illustrative prototype mapping. Do not treat its relationships as verified until claim-level sources have been reviewed."
                    if st.session_state.language == "English" else
                    "Hồ sơ học thuật hiện là bản đồ minh họa trong nguyên mẫu. Không xem các mối liên hệ là đã được xác minh cho đến khi từng nhận định được đối chiếu với nguồn cụ thể."
                )

elif page == tr("compare"):
    st.title(tr("compare"))
    selected = st.multiselect(tr("choosemajors"),list(MAJORS),max_selections=3)
    if len(selected)>=2:
        fields = [("cluster",tr("cluster")),("overview",tr("mainfocus")),
                  ("academic_foundations", "Academic foundations" if st.session_state.language == "English" else "Nền tảng học thuật"),
                  ("related_disciplines", "Related fields" if st.session_state.language == "English" else "Các lĩnh vực liên quan"),
                  ("specialized_applications", "Specialized applications" if st.session_state.language == "English" else "Ứng dụng chuyên sâu"),
                  ("research_areas", "Research directions" if st.session_state.language == "English" else "Hướng nghiên cứu"),
                  ("limitations", "Scope and limitations" if st.session_state.language == "English" else "Phạm vi và giới hạn"),
                  ("disciplines",tr("disciplines")),("skills",tr("skills")),("careers",tr("careers"))]
        for field,title in fields:
            st.subheader(title); cols=st.columns(len(selected))
            for col,name in zip(cols,selected):
                with col:
                    shown_name = MAJORS[name].get("name_vi",name) if st.session_state.language == "Tiếng Việt" else name
                    st.markdown(f"**{shown_name}**"); val=MAJORS[name][field]
                    if st.session_state.language == "Tiếng Việt" and field == "overview": val=MAJORS[name].get("overview_vi",val)
                    if st.session_state.language == "Tiếng Việt" and field in ["academic_foundations","related_disciplines","specialized_applications","research_areas","limitations"]: val=MAJORS[name].get(field+"_vi",val)
                    if st.session_state.language == "Tiếng Việt" and field == "cluster": val=MAJORS[name].get("cluster_vi",val)
                    if st.session_state.language == "Tiếng Việt" and field == "skills": val=MAJORS[name].get("skills_vi",val)
                    if st.session_state.language == "Tiếng Việt" and field == "disciplines": val=MAJORS[name].get("disciplines_vi",val)
                    if st.session_state.language == "Tiếng Việt" and field == "careers": val=MAJORS[name].get("careers_vi",val)
                    if val is None: val = []
                    if val is None: val = []
                    st.write(", ".join(val) if isinstance(val,list) else val)
        st.subheader("EMASI subjects to consider" if st.session_state.language == "English" else "Các môn EMASI nên cân nhắc")
        for name in selected:
            info = MAJORS[name]
            shown_name = info.get("name_vi", name) if st.session_state.language == "Tiếng Việt" else name
            st.markdown(f"**{shown_name}**")
            for g in info.get("emasi_subject_guidance", []):
                subject = g.get("subject_en") if st.session_state.language == "English" else g.get("subject_vi")
                role = g.get("role_en") if st.session_state.language == "English" else g.get("role_vi")
                why = g.get("why_en") if st.session_state.language == "English" else g.get("why_vi")
                st.markdown(f"- **{subject} · {role}** — {why}")
    else: st.info(tr("mincompare"))

elif page == tr("reflect"):
    st.title(tr("reflect"))
    lang = st.session_state.language
    en = lang == "English"
    copy = {
        "intro": "Turn what you explored into your own questions and next steps. There are no right or wrong answers.",
        "intro_v": "Biến những điều bạn khám phá thành câu hỏi và bước tiếp theo của riêng mình. Không có câu trả lời đúng hay sai.",
        "step1": "01 · Your exploration", "step1_v": "01 · Khám phá của bạn",
        "step2": "02 · What stood out?", "step2_v": "02 · Điều gì khiến bạn chú ý?",
        "step3": "03 · Your questions", "step3_v": "03 · Những câu hỏi của bạn",
        "step4": "04 · What is still uncertain?", "step4_v": "04 · Điều gì vẫn chưa rõ?",
        "step5": "05 · Your next small step", "step5_v": "05 · Bước nhỏ tiếp theo",
        "major_prompt": "Which majors are you thinking about?", "major_prompt_v": "Bạn đang cân nhắc những ngành học nào?",
        "discovery": "What is one thing you discovered?", "discovery_v": "Một điều bạn vừa khám phá được là gì?",
        "connection": "Which academic connection interested you most, and why?", "connection_v": "Mối liên hệ học thuật nào khiến bạn quan tâm nhất, và vì sao?",
        "questions": "What would you like to understand better?", "questions_v": "Bạn muốn hiểu rõ hơn điều gì?",
        "uncertain": "What are you not sure about yet?", "uncertain_v": "Điều gì bạn vẫn chưa chắc chắn?",
        "next": "Choose one realistic action you could take next.", "next_v": "Chọn một hành động thực tế mà bạn có thể thực hiện tiếp theo.",
        "next_hint": "For example: read one university course description, ask a teacher a question, or try a beginner activity.",
        "next_hint_v": "Ví dụ: đọc mô tả một môn học đại học, hỏi giáo viên một câu hỏi hoặc thử một hoạt động nhập môn.",
        "save": "Save this reflection", "save_v": "Lưu bản suy ngẫm này",
        "saved": "Your reflection has been added to this session's journal.", "saved_v": "Bản suy ngẫm đã được thêm vào nhật ký trong phiên này.",
        "journal": "Your exploration journal", "journal_v": "Nhật ký khám phá của bạn",
        "export": "Download journal (Markdown)", "export_v": "Tải nhật ký (Markdown)",
        "clear": "Clear this draft", "clear_v": "Xóa bản nháp này",
        "draft": "Your draft is kept while this app session remains open. Download your journal if you want to keep it.",
        "draft_v": "Bản nháp được giữ trong khi phiên ứng dụng này còn mở. Hãy tải nhật ký nếu bạn muốn lưu lại.",
        "progress": "Reflection progress", "progress_v": "Tiến độ suy ngẫm",
        "empty": "Your journal is empty for now. Save a reflection when you are ready.", "empty_v": "Nhật ký hiện chưa có nội dung. Hãy lưu bản suy ngẫm khi bạn sẵn sàng.",
        "remove": "Remove", "remove_v": "Xóa",
        "placeholder_discovery": "I noticed that…", "placeholder_discovery_v": "Tôi nhận ra rằng…",
        "placeholder_connection": "I am interested in this connection because…", "placeholder_connection_v": "Tôi quan tâm đến mối liên hệ này vì…",
        "placeholder_questions": "I would like to find out…", "placeholder_questions_v": "Tôi muốn tìm hiểu…",
        "placeholder_uncertain": "I am still unsure about…", "placeholder_uncertain_v": "Tôi vẫn chưa chắc chắn về…",
        "placeholder_next": "My next step will be…", "placeholder_next_v": "Bước tiếp theo của tôi sẽ là…",
        "count": "Saved reflections", "count_v": "Số bản suy ngẫm đã lưu",
        "optional": "You may skip any question. Save whenever you are ready.",
        "optional_v": "Bạn có thể bỏ qua bất kỳ câu hỏi nào. Hãy lưu khi bạn sẵn sàng.",
        "save_warning": "Add at least one thought before saving.",
        "save_warning_v": "Hãy nhập ít nhất một nội dung trước khi lưu.",
        "date_label": "Date", "date_label_v": "Ngày",
        "remove_confirm": "Remove this reflection?", "remove_confirm_v": "Xóa bản suy ngẫm này?",
        "all_fields_optional": "All sections are optional; this journal is for your own thinking, not an assessment.",
        "all_fields_optional_v": "Tất cả các phần đều không bắt buộc; nhật ký này dành cho suy nghĩ của bạn, không phải bài đánh giá."
    }
    def rc(k):
        return copy.get(k if en else k+"_v", copy.get(k, ""))
    st.write(rc("intro"))
    st.caption(rc("all_fields_optional"))
    st.caption(rc("optional"))
    st.progress(0.0, text=rc("progress"))
    st.subheader(rc("step1"))
    majors_now = st.multiselect(
        rc("major_prompt"), list(MAJORS),
        format_func=lambda x: x if en else MAJOR_TRANSLATIONS.get(x, x),
        key="reflection_majors"
    )
    st.caption(("You can select more than one, or leave this blank if you are still exploring." if en else "Bạn có thể chọn nhiều ngành hoặc để trống nếu vẫn đang khám phá."))
    st.subheader(rc("step2"))
    discovery = st.text_area(rc("discovery"), key="reflection_discovery", placeholder=rc("placeholder_discovery"), height=90)
    connection = st.text_area(rc("connection"), key="reflection_connection", placeholder=rc("placeholder_connection"), height=90)
    st.subheader(rc("step3"))
    questions = st.text_area(rc("questions"), key="reflection_questions", placeholder=rc("placeholder_questions"), height=90)
    st.subheader(rc("step4"))
    uncertain = st.text_area(rc("uncertain"), key="reflection_uncertain", placeholder=rc("placeholder_uncertain"), height=90)
    st.subheader(rc("step5"))
    st.caption(rc("next_hint"))
    next_step = st.text_area(rc("next"), key="reflection_next_step", placeholder=rc("placeholder_next"), height=90)
    fields = [bool(majors_now), bool(discovery.strip()), bool(connection.strip()), bool(questions.strip()), bool(uncertain.strip()), bool(next_step.strip())]
    st.progress(sum(fields)/len(fields), text=f"{rc('progress')}: {sum(fields)}/{len(fields)}")
    st.caption(rc("draft"))
    if "reflection_journal" not in st.session_state:
        st.session_state.reflection_journal = []
    col1, col2 = st.columns([2,1])
    with col1:
        if st.button(rc("save"), type="primary", use_container_width=True):
            if not any(fields):
                st.warning(rc("save_warning"))
            else:
                from datetime import datetime
                entry = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "majors": majors_now,
                         "discovery": discovery.strip(), "connection": connection.strip(),
                         "questions": questions.strip(), "uncertainty": uncertain.strip(), "next_step": next_step.strip()}
                st.session_state.reflection_journal.append(entry)
                st.success(rc("saved"))
    with col2:
        if st.button(rc("clear"), use_container_width=True):
            for key in ["reflection_majors","reflection_discovery","reflection_connection","reflection_questions","reflection_uncertain","reflection_next_step"]:
                st.session_state.pop(key, None)
            st.rerun()
    st.divider()
    st.subheader(rc("journal"))
    journal = st.session_state.reflection_journal
    st.metric(rc("count"), len(journal))
    if not journal:
        st.info(rc("empty"))
    else:
        journal_title = "Horizon — Personal Exploration Journal" if en else "Horizon — Nhật ký khám phá cá nhân"
        lines = [f"# {journal_title}", ""]
        labels = (
            [("majors","Majors I am exploring"),("discovery","What I discovered"),("connection","Connections that interested me"),("questions","Questions I still have"),("uncertainty","What is still uncertain"),("next_step","My next step")]
            if en else
            [("majors","Các ngành tôi đang tìm hiểu"),("discovery","Điều tôi đã khám phá"),("connection","Những mối liên hệ khiến tôi quan tâm"),("questions","Những câu hỏi tôi vẫn còn"),("uncertainty","Điều tôi chưa chắc chắn"),("next_step","Bước tiếp theo của tôi")]
        )
        for idx, entry in enumerate(journal, 1):
            st.markdown(f"**{idx}. {entry['date']}**")
            for key,label in labels:
                val = entry[key]
                if val:
                    shown = ", ".join(val) if isinstance(val,list) else val
                    st.markdown(f"**{label if en else {'majors':'Ngành học đang tìm hiểu','discovery':'Điều tôi khám phá','connection':'Mối liên hệ khiến tôi quan tâm','questions':'Câu hỏi còn lại','uncertainty':'Điều chưa chắc chắn','next_step':'Bước tiếp theo'}[key]}**  \n{shown}")
            lines.extend([f"## Reflection {idx} — {entry['date']}", ""])
            for key,label in labels:
                val=entry[key]
                if val:
                    export_value = (", ".join(MAJOR_TRANSLATIONS.get(x, x) for x in val) if isinstance(val,list) and not en
                                    else (", ".join(val) if isinstance(val,list) else val))
                    lines.extend([f"### {label}", export_value, ""])
        st.download_button(rc("export"), "\n".join(lines), file_name="horizon_exploration_journal.md", mime="text/markdown")

elif page == tr("about"):
    st.title(tr("about_title"))
    st.subheader(tr("about_sub"))
    st.markdown("---")
    st.header(tr("mission_title")); st.write(tr("mission"))
    st.header(tr("how_title")); st.write(tr("how"))
    st.header(tr("principles_title")); st.write(tr("principles"))
    st.header(tr("database_title")); st.write(tr("database"))
    st.caption(tr("feedback"))
    st.markdown("---")
    st.subheader("About the Creator" if st.session_state.language == "English" else "Về người sáng lập")
    st.markdown("**Vivian Hoang**  \nFounder & Project Developer" if st.session_state.language == "English" else "**Vivian Hoang**  \nNgười sáng lập và phát triển dự án")
    st.caption("Horizon is a student-led prototype. Its sample relationships are exploratory and are being reviewed; they should not be treated as verified university requirements." if st.session_state.language == "English" else "Horizon là nguyên mẫu do học sinh phát triển. Các mối liên hệ mẫu mang tính khám phá và đang được rà soát; không nên xem đây là yêu cầu chính thức đã được xác minh của các trường đại học.")
