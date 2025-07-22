import datetime
import os
from nataly import NatalChart, to_utc

# === USER MUST SET THIS ===
# Path to directory containing Swiss Ephemeris .se1 files (e.g. seas_18.se1, sepl_18.se1, ...)
ephe_path = "/Users/goker/codes/nataly/ephe"  # <-- SET THIS TO YOUR EPHEMERIS DIRECTORY

# Check ephemeris directory and files
required_files = [
    "seas_18.se1", "sepl_18.se1", "semo_18.se1", "seplm18.se1", "semom18.se1"
]
if not os.path.isdir(ephe_path):
    raise RuntimeError(f"Ephemeris directory not found: {ephe_path}")
missing = [f for f in required_files if not os.path.isfile(os.path.join(ephe_path, f))]
if missing:
    raise RuntimeError(f"Missing ephemeris files in {ephe_path}: {missing}\nPlease download from https://www.astro.com/ftp/swisseph/ephe/")

def print_bodies_table(chart, title):
    print(f"\n=== {title} ===")
    print(f"{'Body':<12} {'Type':<10} {'Sign':<12} {'House':<5} {'Dignity':<10}")
    for body in chart.bodies_dict.values():
        print(f"{body.name:<12} {body.body_type:<10} {body.sign.name:<12} {body.house:<5} {body.dignity or '-':<10}")

def print_aspects_table(chart1, chart2=None, title="Aspects"):
    from nataly import AstroEngine
    engine = AstroEngine()
    if chart2:
        aspects = engine.get_aspects(chart1.bodies_dict, chart2.bodies_dict)
    else:
        aspects = engine.get_aspects(chart1.bodies_dict, chart1.bodies_dict)
    print(f"\n=== {title} ===")
    print(f"{'Body1':<12} {'Aspect':<8} {'Body2':<12} {'Phase':<10} {'Orb':<10}")
    for aspect in aspects:
        phase = "Applying" if aspect.is_applying else "Separating"
        print(f"{aspect.body1.name:<12} {aspect.symbol+' '+aspect.aspect_type:<8} {aspect.body2.name:<12} {phase:<10} {aspect.orb_str:<10}")

def print_distribution_table(chart, dist_type, title):
    if dist_type == "Element":
        dist = chart.element_distribution
    elif dist_type == "Modality":
        dist = chart.modality_distribution
    elif dist_type == "Polarity":
        dist = chart.polarity_distribution
    else:
        return
    print(f"\n=== {title} ===")
    print(f"{'Category':<10} {'Sum':<4} Bodies")
    for cat, data in dist.items():
        names = ', '.join([b.name for b in data['bodies']])
        print(f"{cat:<10} {data['count']:<4} {names}")

def print_quadrant_table(chart, title):
    print(f"\n=== {title} ===")
    print(f"{'Quadrant':<10} {'Sum':<4} Bodies")
    for quad, data in chart.quadrant_distribution.items():
        names = ', '.join([b.name for b in data['bodies']])
        print(f"{quad:<10} {data['count']:<4} {names}")

def print_hemisphere_table(chart, title):
    print(f"\n=== {title} ===")
    print(f"{'Hemisphere':<10} {'Sum':<4} Bodies")
    for hemi, data in chart.hemisphere_distribution.items():
        names = ', '.join([b.name for b in data['bodies']])
        print(f"{hemi:<10} {data['count']:<4} {names}")

def print_cross_reference_table(transit_chart, natal_chart):
    from nataly import AstroEngine
    engine = AstroEngine()
    aspects = engine.get_aspects(transit_chart.bodies_dict, natal_chart.bodies_dict)
    t_bodies = list(transit_chart.bodies_dict.keys())
    n_bodies = list(natal_chart.bodies_dict.keys())
    lookup = {(a.body1.name, a.body2.name): f"{a.symbol} {a.orb_str}" for a in aspects}
    print("\n=== TRANSIT ASPECTS CROSS REFERENCE ===")
    print(f"{'':<12}" + ''.join([f"{n:<12}" for n in n_bodies]))
    for t in t_bodies:
        row = [f"{t:<12}"]
        for n in n_bodies:
            row.append(lookup.get((t, n), "-"))
        print(''.join([f"{cell:<12}" for cell in row]))

def main():
    # User info
    name = "Joe Doe"
    dob = '1990-02-27 09:15'
    tz_offset = '+02:00'
    latitude = 38.4167
    longitude = 27.1500
    # Natal chart
    natal_dt_utc = to_utc(dob, tz_offset)
    natal_chart = NatalChart(
        person_name=name,
        dt_utc=natal_dt_utc,
        lat=latitude,
        lon=longitude,
        ephe_path=ephe_path
    )
    # Transit chart (now, same location and offset)
    now_local = datetime.datetime.now()
    now_str = now_local.strftime('%Y-%m-%d %H:%M')
    transit_dt_utc = to_utc(now_str, tz_offset)
    transit_chart = NatalChart(
        person_name="Current Transit",
        dt_utc=transit_dt_utc,
        lat=latitude,
        lon=longitude,
        ephe_path=ephe_path
    )
    # Print all tables for natal
    print_bodies_table(natal_chart, "NATAL BODIES (ALL)")
    print_aspects_table(natal_chart, None, "NATAL ASPECTS (ALL BODIES)")
    print_distribution_table(natal_chart, "Element", "NATAL ELEMENT DISTRIBUTION")
    print_distribution_table(natal_chart, "Modality", "NATAL MODALITY DISTRIBUTION")
    print_distribution_table(natal_chart, "Polarity", "NATAL POLARITY DISTRIBUTION")
    print_quadrant_table(natal_chart, "NATAL QUADRANT DISTRIBUTION")
    print_hemisphere_table(natal_chart, "NATAL HEMISPHERE DISTRIBUTION")
    # Print all tables for transit
    print_bodies_table(transit_chart, "TRANSIT BODIES (ALL)")
    print_aspects_table(transit_chart, None, "TRANSIT ASPECTS (ALL BODIES)")
    print_distribution_table(transit_chart, "Element", "TRANSIT ELEMENT DISTRIBUTION")
    print_distribution_table(transit_chart, "Modality", "TRANSIT MODALITY DISTRIBUTION")
    print_distribution_table(transit_chart, "Polarity", "TRANSIT POLARITY DISTRIBUTION")
    print_quadrant_table(transit_chart, "TRANSIT QUADRANT DISTRIBUTION")
    print_hemisphere_table(transit_chart, "TRANSIT HEMISPHERE DISTRIBUTION")
    # Print cross reference
    print_cross_reference_table(transit_chart, natal_chart)

if __name__ == "__main__":
    main() 