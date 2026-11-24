"""Educational PDH-complex mechanism data.

The descriptions intentionally use reaction-language and schematic notation
instead of drawing molecular structures that could be chemically misleading.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MechanismStep:
    key: str
    title: str
    description: str
    event: str


PDH_STEPS = (
    MechanismStep(
        "tpp_ylide",
        "TPPのC2位の脱プロトン化",
        "チアゾリウム環のC2位からプロトンが引き抜かれ、共鳴で安定化されたTPPイリドが生じる。",
        "脱プロトン化",
    ),
    MechanismStep(
        "pyruvate_attack",
        "ピルビン酸への求核攻撃",
        "TPPイリドの求核性をもつC2炭素が、ピルビン酸のカルボニル炭素を攻撃する。",
        "求核攻撃・共有結合形成",
    ),
    MechanismStep(
        "decarboxylation",
        "脱炭酸",
        "付加体からCO2が放出され、TPPに結合した2炭素断片が残る。",
        "C-C結合切断・CO2放出",
    ),
    MechanismStep(
        "hydroxyethyl_tpp",
        "ヒドロキシエチルTPPの形成",
        "プロトン移動を経て、ヒドロキシエチルTPPとして2炭素断片が保持される。",
        "プロトン化・中間体形成",
    ),
    MechanismStep(
        "lipoamide_transfer",
        "リポアミドへの酸化的移動",
        "ヒドロキシエチル基が酸化され、リポアミドのジスルフィドにアセチル基が移る。",
        "酸化・アセチル基転移",
    ),
    MechanismStep(
        "coa_transfer",
        "CoAによるアセチル基の受け取り",
        "アセチルリポアミドのチオエステルがCoAと反応し、アセチルCoAを生じる。",
        "チオエステル交換",
    ),
    MechanismStep(
        "fad_reoxidation",
        "FADによるリポアミド再酸化",
        "還元型リポアミドから電子がFADへ渡り、酸化型リポアミドが再生される。",
        "電子移動・FADの還元",
    ),
    MechanismStep(
        "nad_reoxidation",
        "NAD+によるFADH2再酸化",
        "FADH2からNAD+へ電子が渡り、FADとNADHが生じる。",
        "電子移動・NADH形成",
    ),
)


ELECTRON_CHALLENGES = (
    {
        "prompt": "TPPイリドがピルビン酸と反応するとき、電子対はどこからどこへ移動する？",
        "choices": (
            "TPPイリドの求核性C2炭素 → ピルビン酸のカルボニル炭素",
            "ピルビン酸のカルボニル酸素 → TPPのC2炭素",
            "NAD+ → ピルビン酸のメチル炭素",
        ),
        "answer": 0,
        "difficulty": "標準",
        "explanation": "TPPイリドのC2炭素が求核剤、カルボニル炭素が求電子中心です。チアゾリウム環の正電荷とイリドの共鳴安定化が、カルボニルへの共有結合形成を可能にします。",
    },
    {
        "prompt": "脱炭酸で起こる変化として正しいものは？",
        "choices": (
            "C-C結合の電子がCO2側へ移り、CO2が放出される",
            "NADHがNAD+へ酸化され、酸素が放出される",
            "CoAの硫黄が直接CO2を還元する",
        ),
        "answer": 0,
        "difficulty": "応用",
        "explanation": "付加体の電子再配置によりピルビン酸由来のカルボキシ基がCO2として放出されます。TPPはアニオン中間体を安定化するので、単独では起こりにくい脱炭酸を促進できます。",
    },
    {
        "prompt": "FADH2の再酸化で電子を受け取るのは？",
        "choices": ("NAD+", "CoA", "ピルビン酸"),
        "answer": 0,
        "difficulty": "標準",
        "explanation": "PDH複合体ではE3のジヒドロリポイルデヒドロゲナーゼで、FADがリポアミドを再酸化し、続いてFADH2からNAD+へヒドリド相当が移ってNADHが生じます。",
    },
    {
        "prompt": "還元型リポアミドに含まれるジスルフィドの変化として正しいものは？",
        "choices": (
            "ジスルフィドが還元されて2個のスルフヒドリル基になる",
            "ジスルフィドがCO2と結合してカルボキシル化される",
            "スルフヒドリル基がNADHへ直接アセチル化される",
        ),
        "answer": 0,
        "explanation": "リポアミドのジスルフィドがヒドロキシエチル基を酸化的に受け取る過程で還元され、開環したジスルフヒドリル基となります。そのチオールがアセチル基を保持します。",
        "difficulty": "応用",
    },
    {
        "prompt": "PDH反応全体の電子受容体として最終的に還元される分子は？",
        "choices": ("NAD+", "CoA", "リポアミド"),
        "answer": 0,
        "explanation": "ピルビン酸の酸化に伴う電子は、リポアミドとFADを経てNAD+へ移り、NADHとしてまとめられます。CoAは電子ではなくアセチル基の受容体です。",
        "difficulty": "発展",
    },
)


INTERMEDIATES = (
    {
        "name": "TPPイリド",
        "clue": "チアゾリウム環のC2位が脱プロトン化され、求核性を示す。",
        "choices": ("TPPイリド", "ヒドロキシエチルTPP", "アセチルCoA"),
        "answer": "TPPイリド",
        "next": "ピルビン酸のカルボニル炭素を攻撃する。",
    },
    {
        "name": "ヒドロキシエチルTPP",
        "clue": "脱炭酸後の2炭素断片をTPP上に保持する中間体。",
        "choices": ("TPPイリド", "ヒドロキシエチルTPP", "還元型FAD"),
        "answer": "ヒドロキシエチルTPP",
        "next": "酸化されながらリポアミドへアセチル基を渡す。",
    },
    {
        "name": "アセチルリポアミド",
        "clue": "酸化された2炭素断片をチオエステルとして保持する中間体。",
        "choices": ("アセチルリポアミド", "TPPイリド", "NADH"),
        "answer": "アセチルリポアミド",
        "next": "CoAとのチオエステル交換でアセチルCoAを生じる。",
    },
)


RESEARCH_CHALLENGES = (
    {
        "prompt": "ヒドロキシエチルTPPの次に起こる反応は？",
        "choices": (
            "リポアミドへの酸化的アセチル基移動",
            "直ちにDNAへアセチル基を移動",
            "FADを使わずにNADPHを生成",
        ),
        "answer": 0,
        "difficulty": "標準",
        "explanation": "E2（ジヒドロリポイルトランスアセチラーゼ）のリポアミドで酸化的アセチル基移動が進みます。TPPは交換可能な補因子として中間体を放出し、リポアミドがアセチル基を受け取ります。",
    },
    {
        "prompt": "PDH複合体の最終的な還元生成物は？",
        "choices": ("NADH", "NADPH", "FAD"),
        "answer": 0,
        "difficulty": "標準",
        "explanation": "E3でFADH2がNAD+を還元し、NADHが生成されます。FADは酵素上での電子中継分子であり、反応後も酵素に結合したままで再酸化されます。",
    },
    {
        "prompt": "アセチルリポアミドに対してCoAが作用する反応として正しいものは？",
        "choices": (
            "CoAのチオール基がアセチル基を求核攻撃し、アセチルCoAを生成する",
            "CoAがTPPと共有結合してCO2を放出する",
            "CoAがピルビン酸を直接脱炭酸する",
        ),
        "answer": 0,
        "explanation": "CoAの-SHがアセチルリポアミドのチオエステルを求核攻撃し、チオエステル交換でアセチルCoAと還元型リポアミドを生じます。",
        "difficulty": "応用",
    },
    {
        "prompt": "ある実験でPDHの脱炭酸段階を阻害したが、E3は正常であるとき、最も直接的に減少する反応産物は？",
        "choices": (
            "ヒドロキシエチルTPPとアセチルCoA",
            "NADHのみで、アセチルCoAは増加",
            "酸素とATPが直接生成",
        ),
        "answer": 0,
        "explanation": "脱炭酸段階が止まればヒドロキシエチルTPPが生成せず、下流のアセチル基移動もNADH生成も起こりません。E3だけ正常でも基質が供給されなければ還元生成物を生じません。",
        "difficulty": "発展",
    },
    {
        "prompt": "PDHを阻害した筋細胞でピルビン酸が蓄積した。乳酸発酵が増える理由として最も適切なものは？",
        "choices": (
            "細胞質のNADHを再酸化し、解糖系を継続するため",
            "乳酸がミトコンドリアでCO2を直接生成するため",
            "乳酸がアセチルCoAへ直接変換されるため",
        ),
        "answer": 0,
        "explanation": "PDH阻害でピルビン酸の酸化経路が絞られると、乳酸脱水素酵素がピルビン酸を乳酸へ還元し、NADHをNAD+へ再酸化して解糖系の進行を補います。",
        "difficulty": "発展",
    },
)
