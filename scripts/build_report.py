"""Build the Work 3 report as a print-ready A4 PDF."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "report" / "Work3_Padding_Oracle_Report.pdf"
ASSETS = ROOT / "assets"

NAVY = colors.HexColor("#10243e")
BLUE = colors.HexColor("#1f5a94")
TEAL = colors.HexColor("#0f766e")
ORANGE = colors.HexColor("#b45309")
RED = colors.HexColor("#991b1b")
GREY = colors.HexColor("#64748b")
LIGHT = colors.HexColor("#f8fafc")
PALE_BLUE = colors.HexColor("#eff6ff")
PALE_ORANGE = colors.HexColor("#fff7ed")
PALE_GREEN = colors.HexColor("#f0fdf4")
PALE_RED = colors.HexColor("#fef2f2")
LINE = colors.HexColor("#d7dee8")

pdfmetrics.registerFont(TTFont("SegoeUI", r"C:\Windows\Fonts\segoeui.ttf"))
pdfmetrics.registerFont(TTFont("SegoeUI-Bold", r"C:\Windows\Fonts\segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("SegoeUI-Italic", r"C:\Windows\Fonts\segoeuii.ttf"))
pdfmetrics.registerFont(TTFont("SegoeUI-BoldItalic", r"C:\Windows\Fonts\segoeuiz.ttf"))
pdfmetrics.registerFont(TTFont("CascadiaMono", r"C:\Windows\Fonts\CascadiaMono.ttf"))
pdfmetrics.registerFontFamily(
    "SegoeUI",
    normal="SegoeUI",
    bold="SegoeUI-Bold",
    italic="SegoeUI-Italic",
    boldItalic="SegoeUI-BoldItalic",
)


BODY = ParagraphStyle(
    "Body",
    fontName="SegoeUI",
    fontSize=9.55,
    leading=13.7,
    textColor=colors.HexColor("#1f2937"),
    alignment=TA_JUSTIFY,
    spaceAfter=5.5,
)
SMALL = ParagraphStyle(
    "Small",
    parent=BODY,
    fontSize=8.2,
    leading=11.2,
    textColor=colors.HexColor("#475569"),
)
H1 = ParagraphStyle(
    "H1",
    fontName="SegoeUI-Bold",
    fontSize=15.2,
    leading=18.5,
    textColor=NAVY,
    spaceBefore=3,
    spaceAfter=8,
    keepWithNext=True,
)
H2 = ParagraphStyle(
    "H2",
    fontName="SegoeUI-Bold",
    fontSize=11.1,
    leading=14,
    textColor=BLUE,
    spaceBefore=8,
    spaceAfter=4,
    keepWithNext=True,
)
CAPTION = ParagraphStyle(
    "Caption",
    fontName="SegoeUI",
    fontSize=7.9,
    leading=10.2,
    textColor=colors.HexColor("#526071"),
    alignment=TA_CENTER,
    spaceBefore=3,
    spaceAfter=7,
)
TABLE_HEAD = ParagraphStyle(
    "TableHead",
    fontName="SegoeUI-Bold",
    fontSize=7.8,
    leading=9.8,
    textColor=NAVY,
)
TABLE_BODY = ParagraphStyle(
    "TableBody",
    fontName="SegoeUI",
    fontSize=7.7,
    leading=9.8,
    textColor=colors.HexColor("#1f2937"),
)
CODE = ParagraphStyle(
    "Code",
    fontName="CascadiaMono",
    fontSize=7.05,
    leading=10.0,
    textColor=colors.HexColor("#dbeafe"),
    backColor=colors.HexColor("#0f172a"),
    borderColor=colors.HexColor("#1e293b"),
    borderWidth=0.7,
    borderPadding=8,
    leftIndent=2,
    rightIndent=2,
    spaceBefore=4,
    spaceAfter=7,
)
TOC_STYLE = ParagraphStyle(
    "TOC",
    fontName="SegoeUI",
    fontSize=9.4,
    leading=16,
    textColor=NAVY,
)
REF = ParagraphStyle(
    "Reference",
    parent=BODY,
    fontSize=8.15,
    leading=11.2,
    leftIndent=9,
    firstLineIndent=-9,
    alignment=TA_LEFT,
    spaceAfter=4,
)
COVER_SMALL = ParagraphStyle(
    "CoverSmall",
    fontName="SegoeUI-Bold",
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#7dd3fc"),
)
COVER_TITLE = ParagraphStyle(
    "CoverTitle",
    fontName="SegoeUI-Bold",
    fontSize=30,
    leading=35,
    textColor=colors.white,
    spaceAfter=9,
)
COVER_SUB = ParagraphStyle(
    "CoverSub",
    fontName="SegoeUI",
    fontSize=12,
    leading=18,
    textColor=colors.HexColor("#dbeafe"),
)
COVER_META = ParagraphStyle(
    "CoverMeta",
    fontName="SegoeUI",
    fontSize=9.4,
    leading=14,
    textColor=colors.white,
)


class Rule(Flowable):
    def __init__(self, width: float, color=LINE, thickness: float = 0.8):
        super().__init__()
        self.width = width
        self.color = color
        self.thickness = thickness
        self.height = 1

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


class ReportDoc(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs):
        super().__init__(filename, pagesize=A4, **kwargs)
        self.toc = TableOfContents()
        self.toc.levelStyles = [TOC_STYLE]
        self.toc.dotsMinLevel = 0

        cover_frame = Frame(23 * mm, 21 * mm, A4[0] - 46 * mm, A4[1] - 42 * mm, id="cover")
        body_frame = Frame(
            16 * mm,
            18 * mm,
            A4[0] - 32 * mm,
            A4[1] - 34 * mm,
            id="body",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        landscape_size = landscape(A4)
        landscape_frame = Frame(
            14 * mm,
            13 * mm,
            landscape_size[0] - 28 * mm,
            landscape_size[1] - 29 * mm,
            id="landscape",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(
            [
                PageTemplate(id="Cover", frames=[cover_frame], onPage=self.cover_page),
                PageTemplate(id="Body", frames=[body_frame], onPage=self.body_page),
                PageTemplate(
                    id="Landscape",
                    frames=[landscape_frame],
                    onPage=self.landscape_page,
                    pagesize=landscape_size,
                ),
            ]
        )

    def cover_page(self, canvas, doc):
        width, height = A4
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, width, height, fill=1, stroke=0)
        canvas.setFillColor(colors.HexColor("#0b3b55"))
        canvas.rect(0, 0, 13 * mm, height, fill=1, stroke=0)
        canvas.setStrokeColor(colors.HexColor("#1e4d6b"))
        canvas.setLineWidth(0.45)
        for x in range(175, 291, 14):
            canvas.line(x * mm, 0, x * mm, height)
        for y in range(20, 281, 14):
            canvas.line(0, y * mm, width, y * mm)
        canvas.setFillColor(colors.HexColor("#0f766e"))
        canvas.rect(23 * mm, height - 35 * mm, 35 * mm, 2.2 * mm, fill=1, stroke=0)
        canvas.restoreState()

    def body_page(self, canvas, doc):
        width, height = A4
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.6)
        canvas.line(16 * mm, height - 12 * mm, width - 16 * mm, height - 12 * mm)
        canvas.setFont("SegoeUI", 7.2)
        canvas.setFillColor(GREY)
        canvas.drawString(16 * mm, height - 9.5 * mm, "Work 3 - Computer Attacks")
        canvas.drawRightString(width - 16 * mm, height - 9.5 * mm, "Padding Oracle Attack")
        canvas.line(16 * mm, 12 * mm, width - 16 * mm, 12 * mm)
        canvas.drawString(16 * mm, 7.8 * mm, "zhuhe | HDU 23320116")
        canvas.drawRightString(width - 16 * mm, 7.8 * mm, f"{doc.page}")
        canvas.restoreState()

    def landscape_page(self, canvas, doc):
        width, height = landscape(A4)
        canvas.saveState()
        canvas.setFont("SegoeUI", 7.2)
        canvas.setFillColor(GREY)
        canvas.drawString(14 * mm, height - 8 * mm, "Work 3 - Computer Attacks | Directed graph")
        canvas.drawRightString(width - 14 * mm, height - 8 * mm, f"{doc.page}")
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "H1":
            text = flowable.getPlainText()
            if text != "Contents":
                self.notify("TOCEntry", (0, text, self.page))


def table(headers, rows, widths, header_fill=PALE_BLUE):
    data = [[Paragraph(value, TABLE_HEAD) for value in headers]]
    for row in rows:
        data.append([Paragraph(str(value), TABLE_BODY) for value in row])
    table_flowable = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table_flowable.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), header_fill),
                ("TEXTCOLOR", (0, 0), (-1, 0), NAVY),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4.2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fbfdff")]),
            ]
        )
    )
    return table_flowable


def callout(text: str, accent=TEAL, fill=PALE_GREEN):
    flowable = Table([[Paragraph(text, BODY)]], colWidths=[178 * mm])
    flowable.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
                ("BOX", (0, 0), (-1, -1), 0.35, colors.HexColor("#e2e8f0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return flowable


def code_block(text: str):
    block = Table([[Preformatted(text, CODE)]], colWidths=[174 * mm], hAlign="LEFT")
    block.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0f172a")),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#1e293b")),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return block


def figure(path: Path, width: float, caption: str):
    from PIL import Image as PILImage

    with PILImage.open(path) as source:
        ratio = source.height / source.width
    image = Image(str(path), width=width, height=width * ratio)
    return KeepTogether([image, Paragraph(caption, CAPTION)])


def cover_story():
    story = [
        Spacer(1, 20 * mm),
        Paragraph("HDU IS LABORATORY", COVER_SMALL),
        Spacer(1, 9 * mm),
        Paragraph("Laboratory Work No. 3", COVER_SUB),
        Spacer(1, 2 * mm),
        Paragraph("Computer Attacks", COVER_SUB),
        Spacer(1, 14 * mm),
        Rule(68 * mm, colors.HexColor("#0f766e"), 2.2),
        Spacer(1, 8 * mm),
        Paragraph("Padding Oracle Attack<br/>on CBC Encryption", COVER_TITLE),
        Paragraph(
            "Recovering plaintext and forging authenticated state through a "
            "padding-validity side channel.",
            COVER_SUB,
        ),
        Spacer(1, 35 * mm),
        Table(
            [
                [Paragraph("VARIANT", COVER_SMALL), Paragraph("3", COVER_META)],
                [Paragraph("STUDENT", COVER_SMALL), Paragraph("zhuhe", COVER_META)],
                [Paragraph("HDU NUMBER", COVER_SMALL), Paragraph("23320116", COVER_META)],
                [Paragraph("DATE", COVER_SMALL), Paragraph("20 October 2026", COVER_META)],
            ],
            colWidths=[46 * mm, 78 * mm],
            rowHeights=[11 * mm] * 4,
            style=TableStyle(
                [
                    ("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.HexColor("#315977")),
                    ("LINEBELOW", (0, -1), (-1, -1), 0.8, colors.HexColor("#315977")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#244b67")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ]
            ),
            hAlign="LEFT",
        ),
    ]
    return story


def build_story(doc: ReportDoc):
    story = cover_story()
    story += [NextPageTemplate("Body"), PageBreak()]

    story += [Paragraph("Contents", H1), doc.toc, PageBreak()]

    story.append(Paragraph("1 Purpose", H1))
    story.append(
        Paragraph(
            "The purpose of this work is to analyze one computer attack in enough detail that its "
            "mechanics, prerequisites, observable transitions, and business consequences can be "
            "explained without ambiguity. The selected attack is the <b>padding oracle attack</b> on "
            "systems that encrypt structured data with CBC mode and PKCS#7 padding. The attack is "
            "represented as a directed graph whose initial state is an idle system, whose intermediate "
            "states are attacker actions and system responses, and whose final states are concrete losses.",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "A controlled localhost service was built to demonstrate the attack rather than merely "
            "describe it. The service encrypts a role-bearing session string, exposes a distinguishable "
            "padding error, and accepts the encrypted value as authoritative state. The exploit recovers "
            "the plaintext without the key and then changes the first plaintext block from "
            "<font name='CascadiaMono' size='8'>role=user</font> to "
            "<font name='CascadiaMono' size='8'>role=root</font>. The final response grants the "
            "administrator view. This produces real evidence for the confidentiality and integrity paths "
            "in the graph.",
            BODY,
        )
    )

    story.append(Paragraph("2 Executive Summary", H1))
    story.append(
        Paragraph(
            "The padding oracle is a chosen-ciphertext side channel. CBC decryption computes "
            "<i>P</i><sub>i</sub> = <i>D</i><sub>K</sub>(<i>C</i><sub>i</sub>) xor "
            "<i>C</i><sub>i-1</sub>. If an application reveals whether the decrypted bytes end with valid "
            "PKCS#7 padding, an attacker can modify the preceding block, test candidate byte values, and "
            "learn one byte of <i>D</i><sub>K</sub>(<i>C</i><sub>i</sub>) per successful test. Repeating "
            "this process recovers the plaintext. The same recovered intermediate bytes allow the attacker "
            "to calculate a forged preceding block for chosen plaintext.",
            BODY,
        )
    )
    summary_data = [
        ["Attack class", "Cryptographic side-channel; chosen-ciphertext and adaptive oracle attack"],
        ["Weakness", "CBC encryption without a prior integrity check; distinguishable padding failures"],
        ["Main precondition", "Attacker can submit modified ciphertext and observe a validity difference"],
        ["Primary losses", "Plaintext disclosure, controlled modification, authentication or authority bypass"],
        ["Prevention", "AEAD such as AES-GCM, or Encrypt-then-MAC with constant-time verification"],
        ["Proof produced", "2 CBC blocks recovered in 4,713 oracle requests; forged role accepted as root"],
    ]
    story.append(table(["Aspect", "Result"], summary_data, [38 * mm, 140 * mm]))

    story.append(Paragraph("3 Attack Profile and Preconditions", H1))
    story.append(
        Paragraph(
            "The attack targets a protocol or application design, not a mathematical break of AES. AES can "
            "remain strong while the composition of CBC, padding validation, error handling, and state "
            "acceptance leaks the protected data. This distinction is central: the cipher is not broken, "
            "but the system's behavior supplies information that the cipher was supposed to hide.",
            BODY,
        )
    )
    profile_rows = [
        ["Affected component", "Server-side decryption of client-controlled ciphertext, typically a cookie, hidden form field, URL parameter, or encrypted token."],
        ["Cryptographic condition", "CBC mode with PKCS#7 padding and no authenticated-encryption construction."],
        ["Oracle condition", "A visible difference between valid and invalid padding, such as status code, error text, response length, redirect, or timing."],
        ["Attacker position", "Network access to the endpoint, a captured ciphertext, and the ability to send many modified versions."],
        ["Knowledge", "Block size, ciphertext boundaries, and usually a rough expectation of the plaintext format."],
        ["Typical impact", "Confidentiality loss, ciphertext forgery, privilege escalation, session manipulation, or account lockout during high-volume probing."],
    ]
    story.append(table(["Item", "Condition"], profile_rows, [43 * mm, 135 * mm], header_fill=PALE_ORANGE))
    story.append(
        callout(
            "<b>Historical evidence.</b> CVE-2010-3332 [4] described detailed ASP.NET decryption errors that "
            "allowed attackers to decrypt and modify ViewState and possibly forge cookies. CVE-2014-3566 [5], "
            "known as POODLE, used CBC padding behavior in SSL 3.0 to recover plaintext through a "
            "man-in-the-middle position. These cases show why the oracle is not a theoretical curiosity.",
            accent=ORANGE,
            fill=PALE_ORANGE,
        )
    )

    story.append(Paragraph("4 Technical Mechanism", H1))
    story.append(
        Paragraph(
            "CBC decryption is deterministic for each ciphertext block, but it is chained: the previous "
            "block is xor-ed with the decrypted block to produce plaintext. The initialization vector (IV) "
            "performs that role for the first plaintext block. An attacker who changes the preceding block "
            "therefore changes the corresponding plaintext block in a predictable way, even though the "
            "attacker does not know the key.",
            BODY,
        )
    )
    story.append(figure(ASSETS / "cbc-decryption.png", 170 * mm, "Figure 1. CBC decryption and the chaining value used by the oracle."))
    story.append(
        callout(
            "<b>Core relation.</b> For block <i>i</i>: "
            "<font name='CascadiaMono' size='8'>P_i = D_K(C_i) xor C_(i-1)</font>. "
            "The attacker controls <font name='CascadiaMono' size='8'>C_(i-1)</font> and observes whether "
            "the resulting padding is valid. The unknown value <font name='CascadiaMono' size='8'>D_K(C_i)</font> "
            "is what the attack recovers one byte at a time.",
            accent=BLUE,
            fill=PALE_BLUE,
        )
    )

    story.append(Paragraph("4.1 PKCS#7 padding and the oracle", H2))
    story.append(
        Paragraph(
            "PKCS#7 pads a message to a multiple of the block size. With a 16-byte block, one missing byte "
            "is encoded as <font name='CascadiaMono' size='8'>01</font>, two missing bytes as "
            "<font name='CascadiaMono' size='8'>02 02</font>, and so on through sixteen missing bytes as "
            "sixteen <font name='CascadiaMono' size='8'>10</font> bytes. A decryptor checks the final byte "
            "and then checks that every padding byte has the same value. If the check fails, the normal "
            "result is a generic decryption failure.",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "The oracle exists when the attacker can tell whether that check passed. Passing validity is a "
            "single bit of information, but it is enough for adaptive queries. A response can be an explicit "
            "message such as <font name='CascadiaMono' size='8'>invalid padding</font>, a different HTTP "
            "status, a redirect, or a timing difference. The exact channel is less important than the fact "
            "that the attacker can separate valid from invalid padding reliably.",
            BODY,
        )
    )

    story.append(Paragraph("4.2 Recovering one byte", H2))
    story.append(
        Paragraph(
            "To recover the last byte of a block, the attacker changes the last byte of the preceding block "
            "and sends up to 256 candidates. The goal is a plaintext ending in padding value "
            "<font name='CascadiaMono' size='8'>01</font>. If candidate <i>g</i> produces valid padding, "
            "then <i>D</i><sub>K</sub>(<i>C</i><sub>i</sub>)[15] xor <i>g</i> = 1, so the intermediate byte "
            "is <i>I</i>[15] = <i>g</i> xor 1. After that byte is known, the attacker targets padding "
            "<font name='CascadiaMono' size='8'>02 02</font>, then "
            "<font name='CascadiaMono' size='8'>03 03 03</font>, and repeats until all sixteen bytes are "
            "known. The formula for every position is <i>I</i>[<i>j</i>] = <i>g</i> xor <i>pad</i>.",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "A practical implementation must handle a false positive at the first byte: a candidate could "
            "create two valid padding bytes instead of one. The demonstration flips a second preceding byte "
            "during the first-byte search so that only a true one-byte pad is accepted. This is a small but "
            "important detail that distinguishes a working exploit from a toy loop.",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "The online cost is bounded by 256 guesses for each byte. For a 16-byte block, the worst case is "
            "4,096 requests per block; with uniformly distributed bytes, the expected number is roughly half "
            "that per byte. The observed two-block run used 4,713 requests, which is consistent with the "
            "expected order of magnitude and includes the extra request for the oracle check.",
            BODY,
        )
    )

    story.append(Paragraph("4.3 Forging chosen plaintext", H2))
    story.append(
        Paragraph(
            "Once the attacker knows a block's intermediate value, no key is needed to make a controlled "
            "change. To obtain a target plaintext block <i>P</i>*, the attacker calculates the preceding "
            "block as <font name='CascadiaMono' size='8'>C*_(i-1) = I_i xor P*_i</font>. For the first "
            "plaintext block, the predecessor is the IV, so changing the IV does not corrupt any earlier "
            "plaintext. For a later block, changing the preceding ciphertext also corrupts the previous "
            "plaintext block; a real exploit may need to account for that constraint, use a tolerant parser, "
            "or forge the preceding block as part of a chain. The demonstration deliberately targets the "
            "first block to isolate the integrity failure.",
            BODY,
        )
    )

    story.append(Paragraph("5 Attacker Sequence and Demonstration", H1))
    story.append(
        Paragraph(
            "The laboratory target is a local Flask service bound to 127.0.0.1. It uses a 256-bit AES key, a "
            "random IV, CBC mode, and PKCS#7 padding. The protected message is "
            "<font name='CascadiaMono' size='8'>role=user;uid=1001;ok=1</font>. The service intentionally "
            "returns <font name='CascadiaMono' size='8'>invalid padding</font> separately from a valid-padding "
            "payload parse error, and it trusts the decrypted role. No real user data or organization is involved.",
            BODY,
        )
    )
    sequence_rows = [
        ["1. Acquire", "Request a session and record the base64 value containing IV and ciphertext."],
        ["2. Confirm", "Flip one ciphertext byte. A 400 invalid-padding response proves the oracle is observable."],
        ["3. Recover", "For each block, submit modified predecessor bytes and search each position for valid padding."],
        ["4. Assemble", "Xor the recovered intermediate block with the real predecessor to obtain plaintext."],
        ["5. Forge", "Calculate a new IV from the recovered intermediate value and the chosen first plaintext block."],
        ["6. Verify", "Submit the forged cookie and observe an authorized administrator response."],
    ]
    story.append(table(["Stage", "Action"], sequence_rows, [30 * mm, 148 * mm]))
    story.append(
        code_block(
            "GET /session\n"
            "POST /account  {\"cookie\": \"<iv||ciphertext in base64>\"}\n\n"
            "# controls used by the exploit\n"
            "probe = previous_block_with_one_byte_flipped + target_ciphertext_block\n"
            "valid_padding = (response.status == 400 and error != \"invalid padding\") or response.status != 400\n"
            "intermediate[position] = guess ^ padding_value\n"
            "plaintext_block = intermediate xor original_previous_block\n"
            "forged_iv = intermediate xor chosen_plaintext_block",
        )
    )
    story.append(
        callout(
            "<b>Observed result.</b> The service returned the original user dashboard, then returned "
            "<font name='CascadiaMono' size='8'>role=root</font> and "
            "<font name='CascadiaMono' size='8'>access=admin console</font> for the forged cookie. "
            "The forged value was not a replay: it contained a new IV and a different plaintext block. "
            "The exploit's 4,713 requests demonstrate the online nature of the attack and its dependence "
            "on an observable oracle.",
            accent=RED,
            fill=PALE_RED,
        )
    )
    story.append(PageBreak())
    story.append(Paragraph("5.1 Recorded evidence", H2))
    story.append(figure(ASSETS / "padding-oracle-evidence.png", 174 * mm, "Figure 2. Local execution: plaintext recovery and privilege change from user to root."))
    evidence_rows = [
        ["original cookie -> HTTP 200", "S0-S1", "The baseline session is valid and returns the user dashboard."],
        ["flipped byte -> HTTP 400 invalid padding", "S2-S3", "The oracle is observable through a distinct padding error."],
        ["block 1 and block 2 output", "S4-S6", "The intermediate blocks are recovered and converted to plaintext."],
        ["recovered plaintext line", "S7-K1", "Confidentiality is lost without possession of the AES key."],
        ["after forgery -> role=root", "S8-S9-K2", "The modified IV is accepted and the authorization decision changes."],
    ]
    story.append(table(["Evidence line", "Graph state", "Interpretation"], evidence_rows, [57 * mm, 26 * mm, 95 * mm]))
    story.append(
        Paragraph(
            "The run used 4,713 HTTP calls against a loopback service. That number is not a performance "
            "benchmark; it shows that the attack is an online, adaptive process. A real target may require "
            "parallelism, connection reuse, or timing analysis, and defensive rate limits can change the "
            "practical cost. The demonstration therefore supports the logical graph rather than claiming "
            "universal timing or exploitability.",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "The service and exploit are contained in the accompanying repository. The target binds only to "
            "127.0.0.1, uses synthetic data, and must not be exposed to a network. The evidence was produced "
            "by the same code shown in the report, so the recovered blocks and the forged response are "
            "reproducible rather than hand-written narrative.",
            BODY,
        )
    )

    story += [NextPageTemplate("Landscape"), PageBreak()]
    story.append(Paragraph("6 Directed-Graph Model", H1))
    story.append(
        Paragraph(
            "The model is a finite directed graph <i>G</i> = (<i>V</i>, <i>E</i>). The vertex set begins with "
            "the idle state <i>S</i><sub>0</sub>, continues through attacker and system states "
            "<i>S</i><sub>i</sub>, and terminates in one of the loss states <i>S</i><sub>k</sub>. "
            "Each edge is labelled with the action or observable response that causes the transition. "
            "The self-loop on S3 represents repeated guesses and repeated block processing.",
            BODY,
        )
    )
    story.append(
        figure(
            ASSETS / "attack-digraph.png",
            250 * mm,
            "Figure 3. Directed graph of the padding oracle attack. Blue is the baseline, orange is attacker or oracle activity, green is recovered secret material, and red is a final loss state.",
        )
    )
    story.append(
        Paragraph(
            "The three terminal paths are intentional: K1 is confidentiality loss, K2 is integrity and "
            "authority loss, and K3 is a conditional availability loss caused by lockouts or resource "
            "pressure. K3 is secondary; not every padding oracle attack produces denial of service.",
            BODY,
        )
    )

    story += [NextPageTemplate("Body"), PageBreak()]
    story.append(Paragraph("6.1 State definitions", H2))
    state_rows = [
        ["S0", "System idle; no attacker influence; legitimate encrypted state exists.", "Baseline"],
        ["S1", "Attacker captures IV || C, for example from a cookie or hidden field.", "Network access and observation"],
        ["S2", "Attacker identifies CBC with PKCS#7 and detects a padding-validity difference.", "Flipped-byte test; error or timing"],
        ["S3", "Attacker submits a modified predecessor block and a target ciphertext block.", "Controlled ciphertext modification"],
        ["S4", "Oracle returns a padding-valid response for a candidate byte.", "One-bit side-channel response"],
        ["S5", "Attacker derives one intermediate byte I[j] = g xor pad and moves to the next position.", "Adaptive query loop"],
        ["S6", "All 16 bytes of a block are recovered; I = D_K(C).", "Sixteen successful positions"],
        ["S7", "Plaintext is assembled using P_i = I_i xor predecessor.", "Confidentiality impact"],
        ["K1", "Attacker has the plaintext, session content, or another protected value.", "Information theft"],
        ["S8", "Attacker calculates C* = I xor P* for a chosen plaintext block.", "Forgery construction"],
        ["S9", "Server validates the forged ciphertext and accepts the altered state.", "No MAC or tag was checked"],
        ["K2", "Attacker changes data, impersonates a role, or obtains unauthorized access.", "Integrity and authority loss"],
        ["K3", "Repeated probing, lockout, or resource pressure denies access to a legitimate user.", "Conditional availability loss"],
    ]
    story.append(table(["State", "Meaning in the system", "Entry condition"], state_rows, [15 * mm, 108 * mm, 55 * mm]))

    story.append(Paragraph("6.2 Transition and path consistency", H2))
    edge_rows = [
        ["S0 -> S1", "Attacker obtains network access and captures an encrypted value."],
        ["S1 -> S2", "The response is inspected; a modified ciphertext produces a distinguishable padding failure."],
        ["S2 -> S3", "The attacker selects a target block and begins controlled modifications."],
        ["S3 -> S3", "Next candidate, next byte, or next block; the query count grows but the state remains in the loop."],
        ["S3 -> S4", "A candidate produces a padding-valid response."],
        ["S4 -> S5", "The intermediate byte is calculated from the successful guess and target padding."],
        ["S5 -> S6", "The block is complete after all positions are recovered."],
        ["S6 -> S7 -> K1", "The recovered intermediate block is xor-ed with the real predecessor; plaintext is assembled."],
        ["S6 -> S8 -> S9 -> K2", "The attacker chooses a target, builds a predecessor, and submits a forged value."],
        ["S3 -> K3", "Only when probing causes a lockout, quota, or resource collapse; this is not guaranteed."],
    ]
    story.append(table(["Transition", "Justification"], edge_rows, [37 * mm, 141 * mm], header_fill=PALE_ORANGE))
    story.append(
        callout(
            "<b>Path verification.</b> The confidentiality path is S0-S1-S2-S3-S4-S5-S6-S7-K1. The "
            "integrity path is S0-S1-S2-S3-S4-S5-S6-S8-S9-K2. The conditional availability path is "
            "S0-S1-S2-S3-K3. The S3 self-loop is not a new endpoint; it repeats the guessing action until "
            "S4 is reached. Every non-loop edge has a concrete action or system response, and no terminal "
            "loss is reachable without a prior oracle observation.",
            accent=BLUE,
            fill=PALE_BLUE,
        )
    )

    story.append(Paragraph("7 Loss Analysis", H1))
    loss_rows = [
        ["K1 - Information theft", "Confidential plaintext, session claims, identifiers, or business data", "The attacker recovers block contents and reconstructs the full message."],
        ["K2 - Modification or unauthorized access", "Integrity of state and authority of the session", "The attacker forges a role-bearing block and the service accepts it as root."],
        ["K3 - Denial of service or access", "Availability and responsiveness", "High-volume oracle attempts can trigger lockouts, throttling, or resource exhaustion."],
    ]
    story.append(table(["Final state", "Asset affected", "Loss mechanism"], loss_rows, [43 * mm, 56 * mm, 79 * mm], header_fill=PALE_RED))
    story.append(
        Paragraph(
            "The demonstration directly realizes K1 and K2. It does not claim that a padding oracle always "
            "causes a denial of service: K3 depends on the surrounding controls and traffic volume. This is "
            "why the graph labels K3 as conditional. The distinction keeps the model defensible: a path is "
            "shown only when the system state can actually transition there.",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "The business impact is broader than one disclosed string. Encrypted cookies often contain "
            "tenant identifiers, user IDs, feature flags, or serialized state. A forged block can change "
            "authorization decisions, while leaked identifiers can support follow-on reconnaissance and "
            "targeted attacks. Because the exploit is online and can be automated, a single weak endpoint "
            "can produce many recovered sessions or repeated privilege changes.",
            BODY,
        )
    )

    story.append(Paragraph("8 Countermeasures", H1))
    story.append(
        Paragraph(
            "The correct remediation is not 'hide the error message' in isolation. Error uniformity makes "
            "the oracle harder to observe, but the application still lacks a cryptographic integrity check. "
            "A safe design verifies authenticity before it decrypts, parses, or trusts any plaintext. "
            "Prevention should be layered so that one missing control does not reopen the entire path.",
            BODY,
        )
    )
    control_rows = [
        ["Primary", "Use an AEAD construction such as AES-GCM or ChaCha20-Poly1305 and verify the tag before parsing.", "Removes the unauthenticated CBC state and turns modification into a hard failure."],
        ["Compatibility", "If CBC must remain, use Encrypt-then-MAC with HMAC-SHA-256 over IV || ciphertext and compare in constant time.", "Rejects forged predecessors before the padding check can become an oracle."],
        ["Failure handling", "Return one generic error for malformed, invalid-tag, and invalid-padding cases; avoid secret-dependent branches and timing leaks.", "Reduces the observable distinction even during migration."],
        ["Operations", "Rate-limit decryption failures, alert on repeated tampering, rotate keys, invalidate old cookies, and add regression tests that flip every ciphertext byte.", "Limits automated probing and removes previously captured credentials after a fix."],
    ]
    story.append(table(["Layer", "Action", "Why it works"], control_rows, [24 * mm, 96 * mm, 58 * mm]))
    story.append(Paragraph("8.1 Verification pattern", H2))
    story.append(
        code_block(
            "# Preferred: authenticated encryption. The tag check happens before parse.\n"
            "plaintext = aes_gcm.decrypt(nonce, ciphertext_with_tag, associated_data)\n"
            "session = parse_session(plaintext)  # only after successful authentication\n\n"
            "# If CBC is unavoidable: Encrypt-then-MAC, then constant-time compare.\n"
            "expected = hmac_sha256(mac_key, iv + ciphertext)\n"
            "if not hmac.compare_digest(expected, received_tag):\n"
            "    reject_with_generic_error()\n"
            "plaintext = cbc_decrypt(key, iv, ciphertext)\n"
            "session = parse_session(remove_pkcs7(plaintext))",
        )
    )
    story.append(
        Paragraph(
            "The local lab should not be deployed. Its key, endpoint, and deliberately distinguishable "
            "padding response are educational artifacts. A production migration would also need to decide "
            "how to handle already-issued cookies: the safest choice is coordinated invalidation and "
            "reissuance, because an attacker may have captured encrypted values before the patch.",
            BODY,
        )
    )

    story.append(Paragraph("9 Conclusion", H1))
    story.append(
        Paragraph(
            "The padding oracle attack shows how a small observable difference becomes a complete "
            "confidentiality and integrity compromise. CBC and PKCS#7 are not inherently malicious, but "
            "they do not authenticate the ciphertext. Once the application treats padding validity as a "
            "user-visible signal and trusts decrypted state, an attacker can turn that signal into a byte-by-byte "
            "decryption oracle and then into a forgery primitive.",
            BODY,
        )
    )
    story.append(
        Paragraph(
            "The directed graph makes the attack auditable. It fixes the baseline S0, names each "
            "intermediate action and response, exposes the self-loop that drives the query cost, and makes "
            "the K1, K2, and conditional K3 outcomes explicit. The most effective defense is equally "
            "structural: authenticate before decrypting, reject tampering before parsing, and remove the "
            "observable oracle rather than merely changing its error text.",
            BODY,
        )
    )
    story.append(
        callout(
            "<b>Takeaway.</b> Encryption without authentication protects against reading ciphertext, not "
            "against modifying it. The padding oracle is a system-design failure, not evidence that AES has "
            "been broken.",
            accent=TEAL,
            fill=PALE_GREEN,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("10 References", H1))
    references = [
        "[1] S. Vaudenay, &quot;Security Flaws Induced by CBC Padding - Applications to SSL, IPSEC, WTLS...,&quot; EUROCRYPT 2002. https://doi.org/10.1007/3-540-46035-7_35",
        "[2] NIST, &quot;Recommendation for Block Cipher Modes of Operation: Methods and Techniques,&quot; SP 800-38A. https://doi.org/10.6028/NIST.SP.800-38A",
        "[3] NIST, &quot;Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC,&quot; SP 800-38D. https://doi.org/10.6028/NIST.SP.800-38D",
        "[4] NVD, &quot;CVE-2010-3332 - ASP.NET Padding Oracle Vulnerability.&quot; https://nvd.nist.gov/vuln/detail/CVE-2010-3332",
        "[5] NVD, &quot;CVE-2014-3566 - POODLE.&quot; https://nvd.nist.gov/vuln/detail/CVE-2014-3566",
        "[6] OWASP, &quot;Cryptographic Storage Cheat Sheet.&quot; https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html",
        "[7] OWASP, &quot;A02:2021 - Cryptographic Failures,&quot; OWASP Top 10. https://owasp.org/Top10/A02_2021-Cryptographic_Failures/",
        "[8] J. Schaad et al., &quot;An Interface and Algorithms for Authenticated Encryption,&quot; RFC 5116. https://www.rfc-editor.org/rfc/rfc5116",
        "[9] MITRE, &quot;CWE-353: Missing Support for Integrity Check.&quot; https://cwe.mitre.org/data/definitions/353.html",
        "[10] MITRE ATT&amp;CK, &quot;T1557: Adversary-in-the-Middle.&quot; https://attack.mitre.org/techniques/T1557/",
    ]
    for reference in references:
        story.append(Paragraph(reference, REF))

    story.append(PageBreak())
    story.append(Paragraph("Appendix A - Review Questions", H1))
    answers = [
        (
            "1. Vulnerability versus exploit",
            "A vulnerability is the weakness itself: unauthenticated CBC encryption plus a distinguishable padding check. An exploit is the concrete method that turns the weakness into an outcome. The digraph primarily models the exploit path through system states, while the missing integrity check and observable error are the vulnerability conditions that make the path possible.",
        ),
        (
            "2. Why S0 and Sk must be explicit",
            "S0 defines the baseline against which all attacker influence is measured. The final states define what counts as a loss. Without both, a diagram can become an unordered collection of attack steps and cannot demonstrate that every path ends in a concrete consequence or that each transition is justified.",
        ),
        (
            "3. Different digraphs for the same attack",
            "A decrypt-only strategy reaches K1 without S8 or S9. A privilege-escalation strategy includes forgery and acceptance. An attacker who targets a later block may add states for repairing or cascading corruption in preceding blocks. A timing-based oracle may replace explicit error states with repeated measurements. The graph changes with strategy, target, and available observation.",
        ),
        (
            "4. Loss categories",
            "This attack directly causes information theft and modification or unauthorized access. It can cause denial of service or access when probing triggers lockout or resource exhaustion, but that path is conditional. The demonstration provides evidence for theft and privilege change, not a guaranteed denial of service.",
        ),
        (
            "5. Value of the digraph for countermeasures",
            "The graph identifies choke points. If the oracle edge S3-S4 is removed, neither K1 nor K2 is reachable through the demonstrated route. If integrity is verified before S9, the forged block cannot be accepted. The graph therefore converts a narrative into testable security properties and makes clear that a control must block all relevant paths, not only one outcome.",
        ),
    ]
    for heading, answer in answers:
        story.append(Paragraph(heading, H2))
        story.append(Paragraph(answer, BODY))

    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = ReportDoc(str(OUTPUT))
    doc.multiBuild(build_story(doc))
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
