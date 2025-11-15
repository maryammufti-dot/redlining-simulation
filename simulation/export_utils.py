# simulation/export_utils.py
import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import folium
import json

def export_csv(student, path="outputs"):
    os.makedirs(path, exist_ok=True)
    fname = os.path.join(path, f"student_{student.identity}_{int(student.history[0]['time'])}.csv")
    keys = ["time","event_id","event","choice","outcome","effects","wealth","education","health"]
    with open(fname, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in student.history:
            r = row.copy()
            r["effects"] = str(r["effects"])
            writer.writerow(r)
    return fname

def export_pdf(student, path="outputs"):
    os.makedirs(path, exist_ok=True)
    fname = os.path.join(path, f"student_{student.identity}_{int(student.history[0]['time'])}.pdf")
    c = canvas.Canvas(fname, pagesize=letter)
    width, height = letter
    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40,y, f"Simulation Summary - Identity: {student.identity} ({student.gender})")
    y -= 24
    c.setFont("Helvetica", 10)
    c.drawString(40,y, student.blurb)
    y -= 24
    c.drawString(40,y, f"Final Scores - Wealth: {student.wealth}   Education: {student.education}   Health: {student.health}")
    y -= 36
    c.drawString(40,y, "Event history:")
    y -= 18
    for row in student.history:
        line = f"{row['event']} -> choice: {row['choice']} -> outcome: {row['outcome']} -> effects: {row['effects']}"
        c.drawString(40,y, line[:100])
        y -= 14
        if y < 60:
            c.showPage()
            y = height - 40
    c.save()
    return fname

def export_map(neighborhood_data, out_html="outputs/map.html"):
    # neighborhood_data is a dict with lat/lon and a label list. We produce a small folium map.
    m = folium.Map(location=[neighborhood_data.get("lat",42.33), neighborhood_data.get("lon",-83.03)], zoom_start=13)
    for spot in neighborhood_data.get("spots",[]):
        folium.Marker([spot["lat"], spot["lon"]], popup=spot["label"]).add_to(m)
    os.makedirs(os.path.dirname(out_html), exist_ok=True)
    m.save(out_html)
    return out_html
