"""
ReportLab PDF Generation Module.
Produces a clean, single-column, ATS-compliant resume PDF designed for maximum ATS parseability.
"""

import io
from typing import Dict
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, HRFlowable


def generate_ats_resume_pdf(resume_data: Dict) -> bytes:
    """
    Generate a professional single-column ATS-friendly resume PDF using ReportLab.
    Returns bytes of the generated PDF document.
    """
    buffer = io.BytesIO()
    
    # 0.5-inch margins (36 points) allow optimal space while retaining ATS readability
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Brand Colors
    primary_color = colors.HexColor("#0052cc")     # Professional Royal Blue
    dark_text = colors.HexColor("#0f172a")         # Near Black Slate
    muted_text = colors.HexColor("#475569")        # Slate Grey
    line_color = colors.HexColor("#cbd5e1")        # Subtle Border Grey
    
    # Typography Styles
    name_style = ParagraphStyle(
        'ResumeName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=dark_text,
        alignment=0  # Left-aligned for single column ATS standard
    )
    
    title_style = ParagraphStyle(
        'ResumeTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=primary_color,
        alignment=0
    )
    
    contact_style = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=muted_text,
        alignment=0
    )
    
    section_title_style = ParagraphStyle(
        'ResumeSectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=primary_color,
        textTransform='uppercase',
        spaceBefore=8,
        spaceAfter=2
    )
    
    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=dark_text
    )
    
    item_header_style = ParagraphStyle(
        'ResumeItemHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=dark_text
    )
    
    item_sub_style = ParagraphStyle(
        'ResumeItemSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=muted_text
    )
    
    bullet_style = ParagraphStyle(
        'ResumeBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=dark_text,
        leftIndent=14,
        firstLineIndent=-10
    )
    
    # ==========================
    # 1. HEADER & CONTACT INFO
    # ==========================
    personal = resume_data.get("personal", {})
    name = personal.get("full_name", "Candidate Name")
    target_role = personal.get("target_role", "Software Professional")
    
    story.append(Paragraph(name, name_style))
    if target_role:
        story.append(Spacer(1, 2))
        story.append(Paragraph(target_role, title_style))
        
    # Build contact items
    contact_parts = []
    if personal.get("email"):
        contact_parts.append(f"Email: {personal.get('email')}")
    if personal.get("phone"):
        contact_parts.append(f"Phone: {personal.get('phone')}")
    if personal.get("location"):
        contact_parts.append(f"Location: {personal.get('location')}")
    if personal.get("linkedin"):
        contact_parts.append(f"LinkedIn: {personal.get('linkedin')}")
    if personal.get("github"):
        contact_parts.append(f"GitHub: {personal.get('github')}")
        
    contact_line = " &nbsp;|&nbsp; ".join(contact_parts)
    story.append(Spacer(1, 4))
    story.append(Paragraph(contact_line, contact_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceAfter=8, spaceBefore=0))
    
    # ==========================
    # 2. PROFESSIONAL SUMMARY
    # ==========================
    summary = resume_data.get("summary", "")
    if summary and summary.strip():
        story.append(Paragraph("PROFESSIONAL SUMMARY", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.6, color=line_color, spaceAfter=5, spaceBefore=1))
        story.append(Paragraph(summary.strip(), body_style))
        story.append(Spacer(1, 8))
        
    # ==========================
    # 3. TECHNICAL & CORE SKILLS
    # ==========================
    tech_skills = resume_data.get("technical_skills", [])
    soft_skills = resume_data.get("soft_skills", [])
    
    if tech_skills or soft_skills:
        story.append(Paragraph("SKILLS & EXPERTISE", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.6, color=line_color, spaceAfter=5, spaceBefore=1))
        
        if tech_skills:
            tech_line = f"<b>Technical Skills:</b> {', '.join(tech_skills)}"
            story.append(Paragraph(tech_line, body_style))
            story.append(Spacer(1, 2))
            
        if soft_skills:
            soft_line = f"<b>Core Competencies:</b> {', '.join(soft_skills)}"
            story.append(Paragraph(soft_line, body_style))
            
        story.append(Spacer(1, 8))
        
    # ==========================
    # 4. WORK EXPERIENCE
    # ==========================
    experiences = resume_data.get("experience", [])
    if experiences:
        story.append(Paragraph("WORK EXPERIENCE", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.6, color=line_color, spaceAfter=5, spaceBefore=1))
        
        for exp in experiences:
            company = exp.get("company", "").strip()
            role = exp.get("designation", "").strip()
            duration = exp.get("duration", "").strip()
            location = exp.get("location", "").strip()
            
            # Sub-header: Role & Company
            header_text = f"<b>{role}</b> &mdash; {company}" if company and role else (role or company)
            sub_meta = f"{duration} &nbsp;|&nbsp; {location}" if (duration and location) else (duration or location)
            
            # Using clean table for left-right alignment
            exp_table_data = [[
                Paragraph(header_text, item_header_style),
                Paragraph(sub_meta, ParagraphStyle('RAlign', parent=item_sub_style, alignment=2))
            ]]
            exp_table = Table(exp_table_data, colWidths=[380, 152])
            exp_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(exp_table)
            
            # Bullets / Responsibilities
            resp_text = exp.get("responsibilities", "")
            if resp_text:
                lines = [l.strip() for l in resp_text.split("\n") if l.strip()]
                for line in lines:
                    clean_line = line.lstrip("-•* ").strip()
                    story.append(Paragraph(f"&bull; {clean_line}", bullet_style))
            story.append(Spacer(1, 6))
            
        story.append(Spacer(1, 4))
        
    # ==========================
    # 5. PROJECTS
    # ==========================
    projects = resume_data.get("projects", [])
    if projects:
        story.append(Paragraph("PROJECTS", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.6, color=line_color, spaceAfter=5, spaceBefore=1))
        
        for proj in projects:
            title = proj.get("title", "").strip()
            tech = proj.get("technologies", "").strip()
            desc = proj.get("description", "").strip()
            
            header_line = f"<b>{title}</b>"
            if tech:
                header_line += f" <font color='#475569'>({tech})</font>"
            story.append(Paragraph(header_line, item_header_style))
            
            if desc:
                lines = [l.strip() for l in desc.split("\n") if l.strip()]
                for line in lines:
                    clean_line = line.lstrip("-•* ").strip()
                    story.append(Paragraph(f"&bull; {clean_line}", bullet_style))
            story.append(Spacer(1, 5))
            
        story.append(Spacer(1, 4))
        
    # ==========================
    # 6. EDUCATION
    # ==========================
    education = resume_data.get("education", [])
    if education:
        story.append(Paragraph("EDUCATION", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.6, color=line_color, spaceAfter=5, spaceBefore=1))
        
        for edu in education:
            deg = edu.get("degree", "").strip()
            field = edu.get("field", "").strip()
            uni = edu.get("university", "").strip()
            year = edu.get("passing_year", "").strip()
            grade = edu.get("grade", "").strip()
            
            deg_title = f"<b>{deg}</b>" + (f" in {field}" if field else "")
            meta_right = year + (f" | {grade}" if grade else "")
            
            edu_table_data = [[
                Paragraph(deg_title, item_header_style),
                Paragraph(meta_right, ParagraphStyle('RAlignEdu', parent=item_sub_style, alignment=2))
            ]]
            edu_table = Table(edu_table_data, colWidths=[380, 152])
            edu_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(edu_table)
            if uni:
                story.append(Paragraph(uni, item_sub_style))
            story.append(Spacer(1, 4))
            
        story.append(Spacer(1, 4))
        
    # ==========================
    # 7. CERTIFICATIONS
    # ==========================
    certs = resume_data.get("certifications", [])
    if certs:
        story.append(Paragraph("CERTIFICATIONS", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.6, color=line_color, spaceAfter=5, spaceBefore=1))
        for cert in certs:
            if cert.strip():
                story.append(Paragraph(f"&bull; {cert.strip()}", bullet_style))
        story.append(Spacer(1, 6))
        
    # Build Document
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
