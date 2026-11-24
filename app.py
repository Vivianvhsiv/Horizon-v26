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
        "compare":"Compare Majors", "about":"About This Website",
        "tagline":"Discover connections. Open new horizons.",
        "intro":"Explore how your interests and current school subjects may connect to academic disciplines, university majors and possible career areas.",
        "layers":"Connection layers", "sample":"Sample majors", "approach":"Approach",
        "steps":"Explore in four steps", "choose":"Choose", "connect":"Connect", "explore":"Explore",
        "compare_step":"Compare",
        "choose_desc":"Select interests and current subjects.", "connect_desc":"Explore academic and career connections.",
        "explore_desc":"Learn about different majors.", "compare_desc":"Compare two or three majors.",
        
        "notice":"This tool supports exploration. It does not measure ability, predict admission or decide which major is right for you.",
        "network_intro":"Choose your interests, current EMASI subjects and any majors you are considering. The map separates your own selections; it does not infer a major match without claim-level evidence.",
        "why_connected":"Why are these connected?", "relationship":"Relationship type", "evidence_status":"Evidence status",
        "sample_notice":"Evidence status: current interest tags are taxonomy labels, not claim-level evidence of a major connection. EMASI subject guidance remains exploratory and no verified subject-to-major connection records are populated. No inferred major matches are shown.",
        "reset":"Reset view", "selected_node":"Selected node", "no_connections":"No direct connections are recorded for this node in the current sample data.",
        "click_hint":"Your selected interests and subjects are highlighted automatically. Click any node to inspect it and focus on its direct connections.",
        "major_intention":"Majors you are considering (up to 3)", "focus_view":"View one major at a time", "focus_view_help":"Choose a major to highlight its own pathway. Other selected majors remain visible but faded.", "undecided":"I have not decided yet (Undecided)", "major_intention_help":"Choose up to three majors from the same database used by the Network Map.",
        "interest":"Interests to explore", "subject":"EMASI subjects currently studied", "generate":"Generate my network",
        "fullmap":"1. Your selected inputs", "mapcaption":"Only your selected interests, current subjects and explicitly chosen majors appear. Unrelated majors are never added as personalized matches.",
        "nodes":"2. Explore nodes", "node_prompt":"Choose a node to inspect", "direct":"Direct connections",
        "focus":"3. Focus on one connection", "related":"Related node", "candidates":"2. Majors you explicitly selected",
        "notranked":"These are only the majors you explicitly selected. They are not ranked or presented as suitability recommendations.",
        "nomatch":"No direct connection is currently recorded in this sample database. You can still browse all majors.",
        "selectfirst":"Select at least one interest, current subject or major you are considering to generate a network.",
        "cluster":"Filter by academic area", "all":"All", "search_major":"Search majors", "related_subjects":"Related subjects",
        "disciplines":"Academic disciplines", "skills":"Relevant skills", "preparation":"Ways to prepare and explore", "careers":"Possible career areas",
        "choosemajors":"Choose two or three majors", "mainfocus":"Main focus", "mincompare":"Choose at least two majors to compare.",
        "areas":"Which majors would you like to explore further?", "questions":"What questions do you still have?",
        "about_title":"About Horizon", "about_sub":"A student-led space for thoughtful academic and career exploration.",
        "mission_title":"Our purpose", "mission":"Choosing a university major can feel complicated. Horizon helps students discover relationships between their interests, current school subjects, academic fields, university majors and possible career areas.",
        "how_title":"How to use the website", "how":"1. Select interests and current subjects. 2. Explore only connections supported by available evidence. 3. Read about majors. 4. Compare options and make your own informed decision.",
        "principles_title":"What this tool does — and does not do",
        "principles":"Horizon is a starting point for exploration, not an assessment or an admissions tool. A connection does not mean a student is suited to a major, and the absence of a connection does not mean a major is unsuitable. Course requirements vary by university and country. Students should check official university information and talk with trusted teachers or advisors.",
        "database_title":"About the sample database", "database":"This prototype contains a limited set of example majors and mapped relationships. Some connections are illustrative and need further review against university curricula and reliable career information. The database will grow over time.",
        "feedback":"This is an evolving student project. Its content and translations may be refined through student feedback.",
        "language":"Language", "footer":"Explore with curiosity. Decide with information."
    },
    "Tiếng Việt": {
        "nav":"Điều hướng", "home":"Trang chủ", "network":"Mạng lưới khám phá của tôi", "majors":"Khám phá ngành học",
        "compare":"So sánh ngành học", "about":"Giới thiệu trang web",
        "tagline":"Khám phá những kết nối. Mở ra những chân trời mới.",
        "intro":"Tìm hiểu cách sở thích và các môn học hiện tại có thể liên hệ với lĩnh vực học thuật, ngành học đại học và các nhóm nghề nghiệp tiềm năng.",
        "layers":"Các lớp kết nối", "sample":"Ngành học mẫu", "approach":"Cách tiếp cận",
        "steps":"Khám phá qua bốn bước", "choose":"Lựa chọn", "connect":"Kết nối", "explore":"Tìm hiểu",
        "compare_step":"So sánh",
        "choose_desc":"Chọn sở thích và các môn đang học.", "connect_desc":"Khám phá kết nối học thuật và nghề nghiệp.",
        "explore_desc":"Tìm hiểu các ngành học khác nhau.", "compare_desc":"So sánh hai hoặc ba ngành học.",
        
        "notice":"Công cụ này hỗ trợ khám phá. Công cụ không đánh giá năng lực, dự đoán khả năng trúng tuyển hay quyết định ngành học phù hợp với bạn.",
        "network_intro":"Chọn sở thích, các môn EMASI hiện đang học và những ngành bạn đang cân nhắc. Bản đồ phân biệt các lựa chọn của bạn; không tự suy ra ngành phù hợp khi chưa có bằng chứng ở cấp độ nhận định.",
        "why_connected":"Vì sao có những kết nối này?", "relationship":"Loại mối liên hệ", "evidence_status":"Tình trạng bằng chứng",
        "sample_notice":"Tình trạng bằng chứng: nhãn sở thích hiện tại là nhãn phân loại, không phải bằng chứng ở cấp độ nhận định về mối liên hệ với ngành. Gợi ý môn học EMASI vẫn mang tính khám phá và hiện chưa có hồ sơ kết nối môn học–ngành đã xác minh. Không hiển thị ngành được suy luận.",
        "reset":"Đặt lại chế độ xem", "selected_node":"Nút đã chọn", "no_connections":"Dữ liệu mẫu hiện tại chưa ghi nhận kết nối trực tiếp cho nút này.",
        "click_hint":"Sở thích và môn học bạn chọn được làm nổi bật tự động. Nhấp vào bất kỳ nút nào để xem chi tiết và tập trung vào các kết nối trực tiếp.",
        "major_intention":"Các ngành học bạn đang cân nhắc (tối đa 3)", "focus_view":"Xem từng ngành học riêng biệt", "focus_view_help":"Chọn một ngành để làm nổi bật lộ trình riêng. Các ngành đã chọn khác vẫn hiển thị nhưng được làm mờ.", "undecided":"Tôi chưa xác định ngành học", "major_intention_help":"Chọn tối đa ba ngành từ cùng cơ sở dữ liệu được sử dụng trong Bản đồ kết nối.",
        "interest":"Sở thích muốn khám phá", "subject":"Các môn học hiện tại", "generate":"Tạo mạng lưới khám phá",
        "fullmap":"1. Các lựa chọn của bạn", "mapcaption":"Chỉ hiển thị sở thích, môn học hiện tại và ngành bạn chủ động chọn. Các ngành không liên quan sẽ không tự động xuất hiện dưới dạng kết quả cá nhân hóa.",
        "nodes":"2. Khám phá các nút", "node_prompt":"Chọn một nút để xem chi tiết", "direct":"Các kết nối trực tiếp",
        "focus":"3. Tập trung vào một kết nối", "related":"Nút liên quan", "candidates":"2. Các ngành bạn đã chủ động chọn",
        "notranked":"Đây chỉ là những ngành bạn đã chủ động chọn. Chúng không được xếp hạng và không phải đề xuất về mức độ phù hợp.",
        "nomatch":"Hiện chưa có mối liên hệ sở thích–ngành hoặc môn EMASI–ngành được xác minh. Các lựa chọn của bạn vẫn hiển thị và hệ thống không tự suy ra ngành học.",
        "selectfirst":"Hãy chọn ít nhất một sở thích, môn học hiện tại hoặc ngành bạn đang cân nhắc để tạo mạng lưới.",
        "cluster":"Lọc theo lĩnh vực học thuật", "all":"Tất cả", "search_major":"Tìm kiếm ngành học", "related_subjects":"Các môn học liên quan",
        "disciplines":"Các lĩnh vực học thuật", "skills":"Kỹ năng liên quan", "preparation":"Cách chuẩn bị và khám phá", "careers":"Các nhóm nghề nghiệp có thể liên quan",
        "choosemajors":"Chọn hai hoặc ba ngành học", "mainfocus":"Trọng tâm chính", "mincompare":"Hãy chọn ít nhất hai ngành để so sánh.",
        "areas":"Bạn muốn tìm hiểu thêm những ngành nào?", "questions":"Bạn vẫn còn câu hỏi nào?",
        "about_title":"Giới thiệu Horizon", "about_sub":"Không gian khám phá học thuật và nghề nghiệp do học sinh chủ động định hướng.",
        "mission_title":"Mục đích của chúng tôi", "mission":"Việc lựa chọn ngành học đại học có thể khá phức tạp. Horizon giúp học sinh khám phá mối liên hệ giữa sở thích, các môn học hiện tại, lĩnh vực học thuật, ngành học đại học và các nhóm nghề nghiệp tiềm năng.",
        "how_title":"Cách sử dụng trang web", "how":"1. Chọn sở thích và các môn học hiện tại. 2. Khám phá những kết nối có bằng chứng hỗ trợ. 3. Tìm hiểu thông tin về các ngành. 4. So sánh lựa chọn và tự đưa ra quyết định có thông tin.",
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

def build_network(selected_interests, selected_subjects, selected_majors=None):
    """Build a browsable full catalogue with carefully labelled exploratory links."""
    selected_majors = [m for m in (selected_majors or []) if m in MAJORS]
    selected_subjects = list(selected_subjects or [])
    nodes, edges = {}, []

    def add_node(kind, label, description=""):
        key = node_id(kind, label)
        if key not in nodes:
            nodes[key] = {"id": key, "type": kind, "label": label, "description": description}
        return key

    def add_edge(source, target, relation, evidence, evidence_refs=None, status="Descriptive profile data"):
        edge = {"source": source, "target": target, "relation": relation, "evidence": evidence,
                "evidence_refs": evidence_refs or [], "evidence_status": status}
        if edge not in edges:
            edges.append(edge)

    student = add_node("student", "Your exploration", "Your interests and current subjects are student-provided inputs, not an aptitude assessment.")
    for interest in selected_interests:
        key = add_node("interest", interest, "An interest selected by the student. No major match is inferred from this input.")
        add_edge(student, key, "interest in", "Student-selected input; no interest-to-major relationship is inferred.")
    for subject in selected_subjects:
        key = add_node("subject", subject, "A current EMASI subject selected by the student.")
        add_edge(student, key, "currently studies", "Student-selected input.")

    # Build the complete catalogue. Shared profile terms intentionally form
    # cross-major discovery paths; they describe academic content, not student fit.
    profile_fields = [
        ("discipline", "disciplines", "disciplines_vi", "Academic disciplines", "Lĩnh vực học thuật"),
        ("foundation", "academic_foundations", "academic_foundations_vi", "Academic foundations", "Nền tảng học thuật"),
        ("related", "related_disciplines", "related_disciplines_vi", "Related disciplines", "Lĩnh vực liên quan"),
        ("application", "specialized_applications", "specialized_applications_vi", "Specialized applications", "Ứng dụng chuyên sâu"),
        ("research", "research_areas", "research_areas_vi", "Research areas", "Hướng nghiên cứu"),
        ("skill", "skills", "skills_vi", "Skills", "Kỹ năng"),
        ("career", "careers", "careers_vi", "Career areas", "Lĩnh vực nghề nghiệp"),
    ]
    for major, info in MAJORS.items():
        major_key = add_node("major", major, info.get("overview", ""))
        cluster = info.get("cluster", "Other")
        cluster_key = add_node("cluster", cluster, "A browsing category used to organize the Horizon major catalogue; not a suitability label.")
        add_edge(cluster_key, major_key, "contains major", "Horizon catalogue category.")
        for kind, field, field_vi, label_en, label_vi in profile_fields:
            values = info.get(field, [])
            values_vi = info.get(field_vi, [])
            if not isinstance(values, list):
                continue
            for index, value in enumerate(values):
                if not isinstance(value, str) or not value.strip():
                    continue
                translated = values_vi[index] if isinstance(values_vi, list) and index < len(values_vi) else value
                detail = f"{label_en}: {value}. Listed in the Horizon profile for {major}. This is descriptive academic/career context, not a student suitability claim."
                element_key = add_node(kind, value, detail)
                add_edge(major_key, element_key, "profile includes", detail)

        # Subject guidance can create an explicitly exploratory path only when
        # the record carries curriculum references. Its scope caveat is retained.
        for guidance in info.get("emasi_subject_guidance", []):
            subject_name = guidance.get("subject_en", "")
            if not subject_name or not any(subject_name.casefold() == chosen.casefold() for chosen in selected_subjects):
                continue
            refs = guidance.get("evidence_refs", [])
            if not refs:
                continue
            subject_key = add_node("subject", subject_name, "A current EMASI subject selected by the student.")
            status = guidance.get("evidence_status_en", "Exploratory curriculum context")
            scope = guidance.get("evidence_scope_en", "")
            why = guidance.get("why_en", "")
            evidence = f"{why} Status: {status}. Scope: {scope} This is an exploratory curriculum-context link, not proof that EMASI teaches the same content or that this subject is an admission prerequisite."
            add_edge(subject_key, major_key, "explore through curriculum context", evidence, refs, status)

    for major in selected_majors:
        add_edge(student, node_id("major", major), "considering", "Student-selected major intention; not a suitability assessment.")
    return nodes, edges, selected_majors
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
    order = ["student","interest","subject","major","discipline","skill","career"]
    return [(f'{n["type"].title()} · {n["label"]}', key) for kind in order
            for key,n in nodes.items() if n["type"] == kind]


MAJOR_TRANSLATIONS = {
    "Cognitive Science":"Khoa học nhận thức", "Psychology":"Tâm lý học", "Computer Science":"Khoa học máy tính", "Data Science":"Khoa học dữ liệu", "Economics":"Kinh tế học", "Biology":"Sinh học", "Mechanical Engineering":"Kỹ thuật cơ khí", "Finance":"Tài chính", "Chemistry":"Hóa học", "Physics":"Vật lý", "Environmental Science":"Khoa học môi trường", "Architecture":"Kiến trúc", "Electrical Engineering":"Kỹ thuật điện", "Civil Engineering":"Kỹ thuật xây dựng", "Political Science":"Khoa học chính trị", "Sociology":"Xã hội học", "Linguistics":"Ngôn ngữ học", "Education":"Giáo dục học", "Accounting":"Kế toán", "Communication & Media Studies":"Truyền thông và nghiên cứu truyền thông"
}

SKILL_TRANSLATIONS = {
    en: vi
    for info in MAJORS.values()
    for en, vi in zip(info.get("skills", []), info.get("skills_vi", []))
}

NODE_TYPE_VI = {
    "student":"Khám phá của bạn", "interest":"Sở thích", "subject":"Các môn học hiện có tại EMASI",
    "major":"Ngành học đại học", "discipline":"Lĩnh vực học thuật", "career":"Lĩnh vực nghề nghiệp", "skill":"Kỹ năng"
}
RELATION_VI = {
    "interest in":"quan tâm đến", "currently studies":"đang học", "considering":"đang cân nhắc", "profile includes":"hồ sơ ngành học gồm",
    "interest connection":"kết nối sở thích", "academic subject connection":"kết nối môn học",
    "draws on":"có nền tảng từ", "may connect to":"có thể liên quan đến"
}

def translated_node_label(node):
    label = node["label"]
    if st.session_state.language == "Tiếng Việt":
        label = MAJOR_TRANSLATIONS.get(label, SUBJECT_TRANSLATIONS.get(label, INTEREST_TRANSLATIONS.get(label, DISCIPLINE_TRANSLATIONS.get(label, CAREER_TRANSLATIONS.get(label, SKILL_TRANSLATIONS.get(label, label))))))
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
        # focus_keys are the explicitly selected inputs and the student node.
        adjacent.update(focus_keys or [])
        # Highlight the selected major and its own profile elements only.
        # No interest-to-major or subject-to-major matches are inferred.
        for edge in edges:
            if edge["source"] in adjacent:
                adjacent.add(edge["target"])
            elif edge["target"] in adjacent:
                adjacent.add(edge["source"])

    palette = {
        "student":"#315B83", "interest":"#8D7DB8", "subject":"#6D9C98",
        "major":"#C18B4A", "discipline":"#B87575", "career":"#7187A6", "skill":"#B28B9C"
    }
    graph_nodes = []
    for key, item in nodes.items():
        active = key in adjacent if (selected_key or focus_keys) else True
        color = palette.get(item["type"], "#8393A6") if active else "#D9DEE5"
        border = "#172B4D" if key == selected_key else "#FFFFFF"
        size = 31 if key == selected_key else (23 if active else 17)
        display_label = item["label"]
        if st.session_state.language == "Tiếng Việt":
            display_label = MAJOR_TRANSLATIONS.get(display_label, SUBJECT_TRANSLATIONS.get(display_label, INTEREST_TRANSLATIONS.get(display_label, DISCIPLINE_TRANSLATIONS.get(display_label, CAREER_TRANSLATIONS.get(display_label, SKILL_TRANSLATIONS.get(display_label, display_label))))))
        graph_nodes.append(Node(
            id=key, label=display_label, title=(MAJORS.get(item["label"], {}).get("overview_vi", item["description"]) if st.session_state.language == "Tiếng Việt" and item["type"] == "major" else display_label),
            size=size,
            color={"background":color, "border":border, "highlight":{"background":color,"border":"#172B4D"}},
            borderWidth=3 if key == selected_key else 1,
            font={"color":"#17263D" if active else "#A6AFBA", "size":15 if active else 12}
        ))

    graph_edges = []
    for edge in edges:
        if selected_key or focus_keys:
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
    pages = [tr("home"),tr("network"),tr("majors"),tr("compare"),tr("about")]
    page = st.radio(tr("nav"), pages)
    st.divider()
    st.caption(tr("footer"))

if page == tr("home"):
    st.markdown(f"""<div class="hero"><div style="font-size:2.3rem; margin-bottom:.4rem;">⌒✦</div><h1>Horizon</h1><h3>{tr("tagline")}</h3><p>{tr("intro")}</p></div>""", unsafe_allow_html=True)
    st.write("")
    features = {
      "English":[("Student-centered","You explore and decide at your own pace."),("Connection-based","See how interests, subjects and majors relate."),("Exploratory, not decisive","Explore, compare and make your own informed decision."),("Bilingual support","Available in English and Vietnamese.")],
      "Tiếng Việt":[("Lấy học sinh làm trung tâm","Bạn tự khám phá và đưa ra lựa chọn theo nhịp độ của mình."),("Dựa trên các mối liên hệ","Tìm hiểu cách sở thích, môn học và ngành học kết nối với nhau."),("Khuyến khích khám phá","Tìm hiểu, so sánh và tự đưa ra quyết định có thông tin."),("Hỗ trợ song ngữ","Có thể sử dụng bằng tiếng Anh và tiếng Việt.")]
    }
    feature_cols=st.columns(4)
    for col,(heading,body) in zip(feature_cols,features[st.session_state.language]):
        with col:
            st.markdown(f"### {heading}")
            st.caption(body)
    st.divider()
    st.subheader(tr("steps"))
    cols = st.columns(4)
    step_icons=["✧","▤","⌘","⚖"]
    for col,icon,title,desc in zip(cols,step_icons,[tr("choose"),tr("connect"),tr("explore"),tr("compare_step")],
        [tr("choose_desc"),tr("connect_desc"),tr("explore_desc"),tr("compare_desc")]):
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
                "The full map keeps all 20 majors visible as browseable context. Your selected inputs and explicitly chosen majors are highlighted; other majors are not personalized matches. No unsupported links are inferred."
                if st.session_state.language == "English" else
                "Bản đồ đầy đủ luôn hiển thị cả 20 ngành để bạn tham khảo. Các lựa chọn của bạn và ngành bạn chủ động chọn được làm nổi bật; những ngành còn lại không phải kết quả cá nhân hóa. Hệ thống không tự suy ra kết nối khi chưa có bằng chứng."
            )
            st.caption(
                "Click a node to inspect its profile relationships. Profile elements describe a major; they are not a suitability score. No unsupported interest-to-major or subject-to-major links are drawn."
                if st.session_state.language == "English" else
                "Nhấp vào một nút để xem các mối liên hệ trong hồ sơ ngành. Những yếu tố này mô tả ngành học, không phải điểm đánh giá mức độ phù hợp. Hệ thống không tự suy ra kết nối sở thích hoặc môn học–ngành khi chưa có bằng chứng."
            )
            st.info(tr("sample_notice"))
            if not candidates:
                st.warning(
                    "No evidence-backed major matches are currently recorded. Your selected inputs remain visible without inferred major connections."
                    if st.session_state.language == "English" else
                    "Hiện chưa có mối liên hệ ngành học được hỗ trợ bằng bằng chứng. Các lựa chọn của bạn vẫn hiển thị riêng, không tự suy ra ngành học."
                )

            selected_key = st.session_state.get("selected_network_node")
            if selected_key not in nodes:
                selected_key = None

            # Focus only on explicit inputs and stated major intentions.
            # No taxonomy-tag overlap is treated as a personalized match.
            focus_keys = [node_id("student", "Your exploration")]
            focus_keys.extend(node_id("interest", x) for x in interests)
            focus_keys.extend(node_id("subject", x) for x in subjects)
            focus_keys.extend(node_id("major", x) for x in intended_majors)
            if intended_majors:
                labels = intended_majors if st.session_state.language == "English" else [MAJORS[m].get("name_vi", m) for m in intended_majors]
                st.success(("These are the majors you explicitly said you are considering: " + ", ".join(labels) + ". This is your stated intention, not a suitability assessment.") if st.session_state.language == "English" else ("Đây là những ngành bạn chủ động cho biết đang cân nhắc: " + ", ".join(labels) + ". Đây là lựa chọn của bạn, không phải đánh giá mức độ phù hợp."))
            elif interests or subjects:
                st.info("Your selected interests and subjects are shown as separate inputs. No major match is inferred without claim-level evidence." if st.session_state.language == "English" else "Sở thích và môn học bạn chọn được hiển thị riêng. Hệ thống không suy ra ngành học khi chưa có bằng chứng ở cấp độ nhận định.")
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
                            st.write(edge["evidence"])
                            st.caption(f'{tr("relationship")}: {relation}')

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
    q = st.text_input(tr("search_major"), placeholder="e.g. Psychology / Tâm lý học" if st.session_state.language == "English" else "Ví dụ: Psychology / Tâm lý học")
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
                st.caption("Illustrative career areas to explore, not guaranteed job outcomes or a ranking of career paths." if st.session_state.language == "English" else "Đây là các lĩnh vực nghề nghiệp mang tính tham khảo để tìm hiểu, không phải cam kết về việc làm hay xếp hạng lộ trình nghề nghiệp.")
            st.markdown(f"**{tr('preparation')}**")
            prep = info.get("preparation_vi",info["preparation"]) if st.session_state.language == "Tiếng Việt" else info["preparation"]
            for item in prep: st.markdown(f"- {item}")
            st.caption(info.get("caveat_vi",info["caveat"]) if st.session_state.language == "Tiếng Việt" else info["caveat"])
            profile_scope = info.get("profile_scope_vi", info.get("profile_scope", "")) if st.session_state.language == "Tiếng Việt" else info.get("profile_scope", "")
            source_status = info.get("source_status_vi", info.get("source_status", "")) if st.session_state.language == "Tiếng Việt" else info.get("source_status", "")
            if source_status:
                st.caption(("Profile evidence status: " if st.session_state.language == "English" else "Tình trạng bằng chứng của hồ sơ: ") + source_status)
            if profile_scope:
                st.caption(profile_scope)

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
            st.markdown("### EMASI subjects students should pay attention to when exploring this major" if st.session_state.language == "English" else "### Các môn học EMASI học sinh nên chú ý khi tìm hiểu ngành này")
            st.caption(info.get("subject_guidance_note_en", "") if st.session_state.language == "English" else info.get("subject_guidance_note_vi", ""))
            inventory_note = info.get("subject_inventory_note_en", "") if st.session_state.language == "English" else info.get("subject_inventory_note_vi", "")
            if inventory_note:
                st.caption(inventory_note)
            audit = info.get("evidence_audit_summary", {})
            audit_status = audit.get("status_en", "") if st.session_state.language == "English" else audit.get("status_vi", "")
            audit_note = audit.get("note_en", "") if st.session_state.language == "English" else audit.get("note_vi", "")
            if audit_status:
                st.info(f"**{audit_status}**\n\n{audit_note}")
            guidance = info.get("emasi_subject_guidance", [])
            if guidance:
                sourced_guidance = sum(1 for item in guidance if item.get("evidence_refs"))
                unsourced_guidance = len(guidance) - sourced_guidance
                if st.session_state.language == "English":
                    st.caption(f"Evidence coverage for this major: {sourced_guidance}/{len(guidance)} subject suggestions have attached curriculum references; {unsourced_guidance} still need claim-level sources. References support university-level context and do not verify EMASI syllabus alignment or admission prerequisites.")
                else:
                    st.caption(f"Mức độ bao phủ bằng chứng cho ngành này: {sourced_guidance}/{len(guidance)} gợi ý môn học có nguồn chương trình đại học đính kèm; {unsourced_guidance} gợi ý vẫn cần nguồn ở cấp độ nhận định. Các nguồn chỉ hỗ trợ bối cảnh chương trình đại học, không xác minh sự tương ứng với đề cương EMASI hoặc điều kiện tuyển sinh.")
                preferred_role_order = ["Strong preparation", "Helpful support", "Pathway-dependent", "Application-dependent", "Specialized application"]
                available_roles = list(dict.fromkeys(g.get("role_en", "") for g in guidance if g.get("role_en")))
                role_order = [role for role in preferred_role_order if role in available_roles]
                role_order.extend(role for role in available_roles if role not in role_order)
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
                                ref_support = ref.get("support_en", "") if st.session_state.language == "English" else ref.get("support_vi", "")
                                if ref_support:
                                    st.caption(("What this source supports: " if st.session_state.language == "English" else "Nội dung được nguồn hỗ trợ: ") + ref_support)
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
        st.subheader("EMASI subjects students should pay attention to when exploring this major" if st.session_state.language == "English" else "Các môn học EMASI học sinh nên chú ý khi tìm hiểu ngành này")
        for name in selected:
            info = MAJORS[name]
            shown_name = info.get("name_vi", name) if st.session_state.language == "Tiếng Việt" else name
            st.markdown(f"**{shown_name}**")
            for g in info.get("emasi_subject_guidance", []):
                subject = g.get("subject_en") if st.session_state.language == "English" else g.get("subject_vi")
                role = g.get("role_en") if st.session_state.language == "English" else g.get("role_vi")
                why = g.get("why_en") if st.session_state.language == "English" else g.get("why_vi")
                st.markdown(f"- **{subject} · {role}** — {why}")
                # Keep subject guidance exploratory and show its supporting context beside the comparison.
                refs = g.get("evidence_refs", [])
                displayed_refs = 0
                for ref in refs:
                    title = ref.get("title", "")
                    institution = ref.get("institution", "")
                    url = ref.get("url", "")
                    # Never render generic placeholder labels or fabricate missing source metadata.
                    if not (title and institution and url):
                        continue
                    displayed_refs += 1
                    st.caption(("Academic context: " if st.session_state.language == "English" else "Bối cảnh học thuật: ") + f"{institution} — {title}")
                    st.markdown(f"  - [{title}]({url})")
                    support = ref.get("support_en", "") if st.session_state.language == "English" else ref.get("support_vi", "")
                    scope = ref.get("scope_en", "") if st.session_state.language == "English" else ref.get("scope_vi", "")
                    if support: st.caption(("Supports: " if st.session_state.language == "English" else "Nguồn hỗ trợ: ") + support)
                    if scope: st.caption(scope)
                if displayed_refs:
                    status = g.get("evidence_status_en", "") if st.session_state.language == "English" else g.get("evidence_status_vi", "")
                    if status: st.caption(("Evidence status: " if st.session_state.language == "English" else "Trạng thái bằng chứng: ") + status)
                else:
                    st.caption("No source is attached to this exploratory subject suggestion yet." if st.session_state.language == "English" else "Gợi ý môn học mang tính khám phá này hiện chưa có nguồn đính kèm.")

        st.divider()
        st.subheader("Academic evidence behind these profiles" if st.session_state.language == "English" else "Bằng chứng học thuật cho các hồ sơ ngành học")
        st.caption(
            "The references below support specific disciplinary or curriculum claims. They do not validate every comparison field, predict personal suitability, or establish universal admission prerequisites."
            if st.session_state.language == "English" else
            "Các nguồn dưới đây hỗ trợ những nhận định cụ thể về lĩnh vực học thuật hoặc chương trình đào tạo. Chúng không xác minh mọi trường thông tin so sánh, dự đoán mức độ phù hợp cá nhân hay xác lập điều kiện tuyển sinh áp dụng chung."
        )
        for name in selected:
            evidence = ACADEMIC_SOURCES.get(name, {})
            shown_name = MAJORS[name].get("name_vi", name) if st.session_state.language == "Tiếng Việt" else name
            with st.expander(shown_name + (" · sources" if st.session_state.language == "English" else " · nguồn")):
                if not evidence or not evidence.get("claims"):
                    st.caption("No reviewed claim-level sources are recorded yet." if st.session_state.language == "English" else "Chưa có nguồn ở cấp độ nhận định đã được rà soát.")
                    continue
                status = evidence.get("status", "") if st.session_state.language == "English" else evidence.get("status_vi", evidence.get("status", ""))
                scope = evidence.get("scope", "") if st.session_state.language == "English" else evidence.get("scope_vi", evidence.get("scope", ""))
                if status: st.caption(("Evidence status: " if st.session_state.language == "English" else "Trạng thái bằng chứng: ") + status)
                if scope: st.write(scope)
                for claim in evidence.get("claims", []):
                    claim_text = claim.get("claim", "") if st.session_state.language == "English" else claim.get("claim_vi", claim.get("claim", ""))
                    claim_type = claim.get("type", "") if st.session_state.language == "English" else claim.get("type_vi", claim.get("type", ""))
                    claim_status = claim.get("status", "") if st.session_state.language == "English" else claim.get("status_vi", claim.get("status", ""))
                    st.markdown(f"**{claim_text}**")
                    if claim_type: st.caption(("Evidence category: " if st.session_state.language == "English" else "Loại bằng chứng: ") + claim_type)
                    if claim_status: st.caption(("Verification: " if st.session_state.language == "English" else "Xác minh: ") + claim_status)
                    for source in claim.get("sources", []):
                        st.markdown(f"- **{source.get('institution', 'Institution')}** — [{source.get('title', 'Academic source')}]({source.get('url', '#')})")
        st.caption(
            "Career areas and skills are presented as exploration prompts; the source register does not imply that every listed item has been independently validated."
            if st.session_state.language == "English" else
            "Các lĩnh vực nghề nghiệp và kỹ năng được trình bày như gợi ý để khám phá; danh mục nguồn không có nghĩa mọi mục đều đã được xác minh độc lập."
        )
    else: st.info(tr("mincompare"))

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
