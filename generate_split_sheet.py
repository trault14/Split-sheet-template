import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

# Dimensions matching the original template
PAGE_WIDTH = 2550
PAGE_HEIGHT = 3629

def draw_text(c, text, x, y, font_name, font_size, color='#000000', anchor='left'):
    c.setFont(font_name, font_size)
    c.setFillColor(HexColor(color))
    if anchor == 'left':
        c.drawString(x, y, text)
    elif anchor == 'center':
        c.drawCentredString(x, y, text)
    elif anchor == 'right':
        c.drawRightString(x, y, text)

def draw_paragraph_top_left(c, p, x, y_top, width):
    w, h = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - h)
    return h

def draw_signature_block(c, x_by, x_line, y_line):
    # READ & AGREED
    draw_text(c, "READ & AGREED:", x_by, y_line + 95, "Helvetica-Bold", 45)
    # By:
    draw_text(c, "By:", x_by, y_line, "Helvetica", 40)
    # Underline
    c.setLineWidth(3)
    c.setStrokeColor(HexColor('#000000'))
    c.line(x_line, y_line, x_line + 836.62, y_line)
    # Print name:
    draw_text(c, "Print name:", x_by, y_line - 90, "Helvetica", 40)

def main():
    pdf_filename = "Split Sheet Template.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # 1. Page Background (White)
    c.setFillColor(HexColor('#FFFFFF'))
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    # 2. Title
    draw_text(c, "WRITER'S SPLIT", 157.65, 3300, "Helvetica-Bold", 96)
    draw_text(c, "CONFIRMATION", 157.65, 3180, "Helvetica-Bold", 96)
    
    # 3. Date Block
    draw_text(c, "Date", 1448.48, 3200, "Helvetica", 45)
    c.setLineWidth(3)
    c.setStrokeColor(HexColor('#000000'))
    c.line(1594.65, 3200, 2342.30, 3200)
    
    # 4. Salutation
    draw_text(c, "Dear Gentlepersons,", 157.65, 3050, "Helvetica", 45)
    
    # 5. Intro Paragraph
    desc_text = (
        "This letter confirms that we, the sole writers of the composition listed below"
        "(the \"Composition\"), agree to the following division of contributors' shares:"
    )
    style_desc = ParagraphStyle(
        name='Desc',
        fontName='Helvetica',
        fontSize=42,
        leading=60,
        textColor=HexColor('#000000')
    )
    desc_p = Paragraph(desc_text, style_desc)
    draw_paragraph_top_left(c, desc_p, 157.65, 2950, 2184.96)
    
    # 6. Composition Box
    c.setLineWidth(3)
    c.setStrokeColor(HexColor('#000000'))
    c.line(539.82, 2672.09, 2342.61, 2672.09)
    draw_text(c, "Composition:", 157.65, 2684, "Helvetica", 52)
    
    # 7. Table Elements
    # Column Definitions: (Title, Width)
    cols = [
        ("Contributor", 450),
        ("Role", 450),
        ("Writing %", 250),
        ("Publishing %", 250),
        ("PRO", 220),
        ("IPI", 220),
        ("Publisher", 359.25)
    ]
    
    table_left = 176.38
    table_width = 2199.25
    table_top = 2530.15
    header_height = 119.32
    row_height = 119.08
    num_rows = 5
    
    # Table Header Background
    c.setFillColor(HexColor('#0c1b2b'))
    c.rect(table_left, table_top - header_height, table_width, header_height, fill=1, stroke=0)
    
    # Draw Header Text & Vertical Lines Coordinates
    current_x = table_left
    col_x_coords = [table_left]
    for title, width in cols:
        center_x = current_x + width / 2
        # Vertically center text in header cell
        draw_text(c, title, center_x, table_top - header_height + 40, "Helvetica-Bold", 36, color='#FFFFFF', anchor='center')
        current_x += width
        col_x_coords.append(current_x)
        
    # Draw Table Grid Lines
    c.setLineWidth(3)
    c.setStrokeColor(HexColor('#000000'))
    
    # Horizontal lines
    c.line(table_left, table_top, table_left + table_width, table_top) # Top border
    c.line(table_left, table_top - header_height, table_left + table_width, table_top - header_height) # Header separator
    for r in range(1, num_rows + 1):
        y = table_top - header_height - r * row_height
        c.line(table_left, y, table_left + table_width, y)
        
    # Vertical lines
    table_bottom = table_top - header_height - num_rows * row_height
    for x in col_x_coords:
        c.line(x, table_top, x, table_bottom)
        
    # 8. Terms Paragraphs
    style_terms = ParagraphStyle(
        name='Terms',
        fontName='Helvetica',
        fontSize=42,
        leading=58,
        textColor=HexColor('#000000')
    )
    
    terms_text1 = (
        "The writers hereby warrant and represent that there are no samples, "
        "interpolations, replays, or other third-party copyrighted material (individually and "
        "collectively referred to as \"Sample(s)\") contained in the Composition. If a Sample "
        "becomes the subject of a copyright claim in connection with the Composition "
        "and/or payment of monies attributable to the Composition, we agree that our "
        "shares in the copyright and/or monies attributable to the Composition shall not be "
        "reduced unless we are the individual party responsible for furnishing such "
        "Sample(s)."
    )
    terms_text2 = (
        "This agreement may be signed in counterparts, and your signature below"
        "indicates your agreement with the above terms."
    )
    
    terms_p1 = Paragraph(terms_text1, style_terms)
    h_terms1 = draw_paragraph_top_left(c, terms_p1, 157.65, 1740, 2184.96)
    
    terms_p2 = Paragraph(terms_text2, style_terms)
    h_terms2 = draw_paragraph_top_left(c, terms_p2, 157.65, 1740 - h_terms1 - 50, 2184.96)
    
    # 9. Signatures Grid
    draw_signature_block(c, 157.65, 255.98, 655.56)   # Left Top
    draw_signature_block(c, 1407.90, 1506.23, 655.56) # Right Top
    draw_signature_block(c, 157.65, 255.98, 248.18)   # Left Bottom
    draw_signature_block(c, 1407.90, 1506.23, 248.18) # Right Bottom
    
    c.save()
    print("PDF generated successfully.")

if __name__ == "__main__":
    main()
