"""Rebuild REPORT.md and the four-page PDF from the existing measured results.
Optional dependency: pip install reportlab
Run plots.py first if the experiment data changed.
"""
import csv
import statistics
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from matplotlib.font_manager import findfont, FontProperties

for name, weight, style in [("BodyFont", "normal", "normal"), ("BodyBold", "bold", "normal"), ("BodyItalic", "normal", "oblique")]:
    pdfmetrics.registerFont(TTFont(name, findfont(FontProperties(family="DejaVu Sans", weight=weight, style=style))))
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / 'results/results.csv').open() as stream:
    rows = list(csv.DictReader(stream))

def value(algorithm, kind, n, field):
    return statistics.median(float(r[field]) for r in rows
                             if r['algorithm'] == algorithm and r['input'] == kind and int(r['n']) == n)

def ms(a, k, n): return f'{value(a,k,n,"time_ms"):.3f}'
def ops(a, k, n): return int(value(a,k,n,'operations'))

plan = (ROOT / 'EXPERIMENT_PLAN.md').read_text()
card = [line.strip('|').split('|') for line in plan.splitlines() if line.startswith('|')][2:]
card = [(a.strip(), b.strip()) for a, b in card]
caption1 = 'Worst-case recursion explodes, while both DP variants have identical cell counts and quadruple their work when length doubles.'
caption2 = 'With m=n/32, an eightfold increase in text length raises worst-case Naive work about 64-fold but KMP work about eightfold.'
caption3 = 'Worst-case recursion and Naive search grow sharply; small random-input timings are noisy and need the counter plots for context.'
prediction_edit = (
    f'The predicted growth is confirmed by the counters: worst-case recursion rises from {ops("recursive","worst",3):,} '
    f'calls at n=3 to {ops("recursive","worst",12):,} at n=12. Both DP variants increase from 16,384 to 1,048,576 '
    'cell updates as n grows from 128 to 1024, exactly 64-fold. Random recursion is not monotonic: the chosen n=6 pair '
    'needs only 29 calls, versus 65 at n=3, because more matching suffix characters bypass branching. Thus one seeded '
    'random pair per size is illustrative, not a statistical average over all possible inputs.')
prediction_search = (
    f'Worst-case Naive comparisons rise from {ops("naive","worst",4096):,} to {ops("naive","worst",32768):,}, '
    f'while KMP rises from {ops("kmp","worst",4096):,} to {ops("kmp","worst",32768):,}; this supports the predicted '
    'quadratic versus linear growth along m=n/32. Both random-input counter curves are approximately linear and close '
    'together. All generated benchmark search cases have zero matches, isolating comparison costs; reference and random '
    'tests separately check successful and overlapping matches. No universal timing advantage is inferred from this sample.')
time_text = (
    f'Times are medians of three nanoTime measurements after one warm-up for each case, recorded with six decimal places '
    f'in milliseconds. Worst-case recursion at n=12 took {ms("recursive","worst",12)} ms; at text n=32768, worst-case '
    f'Naive took {ms("naive","worst",32768)} ms and KMP {ms("kmp","worst",32768)} ms. Small random-search timings do not '
    'increase smoothly. JIT compilation, garbage collection, allocation and shared-host scheduling can affect them; one '
    'warm-up is only a minimal control. Measurements include instrumentation and output-list allocation, but exclude '
    'input generation, validation and CSV writing. Counters give repeatable evidence of growth even when timings vary; '
    'repeatability means identical inputs, answers and counters, not identical elapsed times.')
answers = [
    ('Which input made search slowest, and why?',
     f'The measured Naive maximum was the worst-case pair at n=32768 and m=1024, taking {ms("naive","worst",32768)} ms. '
     'The text contains only A, while the pattern ends in B after many A characters. Each valid naive start therefore '
     'compares the entire pattern before failing, producing (n-m+1)*m comparisons. KMP reuses the prefix information '
     'instead of restarting; this adversarial input is worst for Naive, not a claim that it always gives KMP the highest elapsed time.'),
    ('How large an n could recursive Edit Distance handle?',
     f'The largest tested length was n=m=12, and the worst case completed with {ops("recursive","worst",12):,} calls '
     f'and a median of {ms("recursive","worst",12)} ms. The experiment deliberately stopped at this planned size '
     'because repeated subproblems cause exponential growth. This was a practical experiment cutoff, not a measured '
     'absolute hardware limit or a program failure. Easy identical strings can be much longer because they follow a single diagonal path.'),
    ('What do two rows gain and lose?',
     'Two rows retain only the previous and current DP rows, reducing auxiliary storage from O(n*m) to O(m). '
     'For n=m=1024, this means 2,050 stored integers rather than 1,050,625, excluding Java array headers. '
     'The answer and O(n*m) running time stay the same, but the complete table is discarded. '
     'Therefore this version cannot directly backtrack a sequence of edits without extra work or a different reconstruction algorithm.'),
    ('Which search would you choose for the city platform?',
     'I would choose KMP for exact pattern searches in potentially long logs. Its O(n+m) bound protects the platform '
     'from repetitive texts that force Naive to repeat comparisons. The trade-off is an O(m) LPS array and more code '
     'than Naive, which can be sufficient for very small inputs. For misspelled street-name suggestions, I would use '
     'the two-row Edit Distance separately, since exact substring search does not correct typos.')
]
validation = ('Validation: all 7 JUnit 5 test methods passed, including the provided reference values, edge cases, '
              '100 random short-string edit comparisons and 100 random search comparisons. The CSV contains 120 '
              'measured rows; all three runs for each case have equal counters and results. A second complete execution '
              'also reproduced all non-time CSV fields. Environment: Linux x86_64, Microsoft OpenJDK 21.0.13, Maven 3.9.9; '
              'Java sources target release 17. The original pre-run card is preserved in EXPERIMENT_PLAN.md; no design changes were made.')

md = '# Assignment 4 - City Search & Spell-Check\n\n## Experiment Design Card\n\n'
md += '| Field | Design recorded before the first run |\n|---|---|\n'
md += '\n'.join(f'| {a} | {b} |' for a,b in card) + '\n\n'
md += '## Plots and results\n\n'
for filename,caption in [('01_edit_work.png',caption1),('02_search_work.png',caption2),('03_median_time.png',caption3)]:
    md += f'![{filename}](results/plots/{filename})\n\n{caption}\n\n'
md += '## Prediction vs result\n\n**Edit Distance.** ' + prediction_edit + '\n\n**String search.** ' + prediction_search
md += '\n\n## Measured time\n\n' + time_text + '\n\n## Short answers\n\n'
for question, answer in answers: md += f'### {question}\n\n{answer}\n\n'
md += '## Validation\n\n' + validation + '\n'
(ROOT / 'REPORT.md').write_text(md)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyCustom',fontName='BodyFont',fontSize=9.4,leading=13,spaceAfter=8,textColor=colors.HexColor('#273548')))
styles.add(ParagraphStyle(name='CellCustom',fontName='BodyFont',fontSize=9,leading=12,spaceAfter=0))
styles.add(ParagraphStyle(name='CaptionCustom',fontName='BodyItalic',fontSize=9,leading=12,spaceAfter=14,textColor=colors.HexColor('#41556c')))
styles['Title'].fontName='BodyBold'; styles['Heading1'].fontName='BodyBold'; styles['Heading2'].fontName='BodyBold'
styles['Title'].fontSize=21; styles['Title'].leading=25; styles['Title'].alignment=TA_LEFT
styles['Heading1'].fontSize=15; styles['Heading1'].leading=19; styles['Heading1'].textColor=colors.HexColor('#173b61')
styles['Heading2'].fontSize=11; styles['Heading2'].leading=15
def para(text, style='BodyCustom'): return Paragraph(escape(text),styles[style])
story=[]
story += [para('City Search & Spell-Check','Title'),para('DAA Assignment 4 | Dynamic Programming and String Algorithms'),para('Experiment Design Card','Heading1')]
table = Table([[para(a,'CellCustom'),para(b,'CellCustom')] for a,b in card],colWidths=[100,415])
table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(0,-1),colors.HexColor('#edf3f8')),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#becbd6')),('INNERGRID',(0,0),(-1,-1),.3,colors.HexColor('#d7dfe7')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story += [table,Spacer(1,12),para('Recorded before measurements in the first Git commit. No changes to the experimental design were made after measurements.'),PageBreak()]
story += [para('Measured operation counts','Heading1')]
for filename,caption in [('01_edit_work.png',caption1),('02_search_work.png',caption2)]:
    story += [Image(str(ROOT/'results/plots'/filename),width=515,height=175.1),para(caption,'CaptionCustom')]
story += [para('Prediction vs result','Heading1'),para('Edit Distance','Heading2'),para(prediction_edit),para('String search','Heading2'),para(prediction_search),PageBreak()]
story += [para('Timing results','Heading1'),Image(str(ROOT/'results/plots/03_median_time.png'),width=515,height=150.2),para(caption3,'CaptionCustom'),para('Largest tested size: median of three runs','Heading2')]
summary = [['Algorithm / input','n','Counter value','Median (ms)']]
for a,n in [('recursive',12),('table',1024),('two_rows',1024),('naive',32768),('kmp',32768)]:
    for k in ['random','worst']: summary.append([f'{a} / {k}',str(n),f'{ops(a,k,n):,}',ms(a,k,n)])
t=Table([[para(c,'CellCustom') for c in row] for row in summary],colWidths=[190,60,145,120])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e0ebf5')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f7f9')]),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story += [t,Spacer(1,12),para('Counter units: calls (recursive), interior cell updates (DP), character comparisons (search).'),para('Why time is not the only evidence','Heading2'),para(time_text),PageBreak()]
story += [para('Short answers and validation','Heading1')]
for question, answer in answers: story += [para(question,'Heading2'),para(answer)]
story += [para('Validation and reproducibility','Heading2'),para(validation)]

def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#d0dae4'));canvas.line(40,36,555,36)
    canvas.setFont('BodyFont',7);canvas.setFillColor(colors.HexColor('#526779'))
    canvas.drawString(40,24,'DAA Assignment 4 | See README.md for student details and AI acknowledgement')
    canvas.drawRightString(555,24,str(doc.page))

doc=SimpleDocTemplate(str(ROOT/'REPORT.pdf'),pagesize=(595.28,841.89),leftMargin=40,rightMargin=40,topMargin=36,bottomMargin=48,
                      title='DAA Assignment 4 - City Search and Spell-Check',author='Assignment Author')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Generated REPORT.md and REPORT.pdf')
