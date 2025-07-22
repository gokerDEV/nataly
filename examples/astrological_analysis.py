"""
Astrological Chart Analysis Tool

This module provides comprehensive astrological chart analysis including:
- Natal chart calculations
- Transit chart calculations (optional)
- Aspect analysis between natal and transit charts
- Distribution analysis (elements, modalities, polarities, quadrants, hemispheres)
- House analysis
- Celestial body positions and dignities

The tool uses the nataly library for astrological calculations and Swiss Ephemeris
for planetary positions.
"""

import datetime
import os
from typing import Dict, List, Optional, Tuple
from nataly import NatalChart, create_orb_config, BodyFilter, to_utc
from nataly.constants import ASTROLOGICAL_BODY_GROUPS, ANGLES_SYMBOLS, SIGNS

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

class AstrologicalAnalyzer:
    """
    A comprehensive astrological analysis class that generates detailed reports
    for natal and transit charts.
    """
    
    def __init__(self):
        """Initialize the analyzer with default settings."""
        self.orb_config = create_orb_config()
    
    def parse_birth_data(self, name: str, birth_date: str, birth_time: str, 
                        latitude: float, longitude: float, timezone: str) -> Tuple[str, datetime.datetime]:
        """
        Parse birth data and convert to UTC datetime.
        
        Args:
            name: Person's name
            birth_date: Birth date in YYYY-MM-DD format
            birth_time: Birth time in HH:MM format (24-hour)
            latitude: Birth location latitude
            longitude: Birth location longitude
            timezone: Birth location timezone (e.g., 'Europe/Istanbul')
            
        Returns:
            Tuple of (name, utc_datetime)
        """
        # timezone is now an offset string like '+02:00'
        dt_str = f"{birth_date} {birth_time}"
        utc_datetime = to_utc(dt_str, timezone)
        return name, utc_datetime
    
    def create_charts(self, natal_data: Tuple[str, datetime.datetime, float, float], 
                     transit_data: Optional[Tuple[str, datetime.datetime, float, float]] = None) -> Tuple[NatalChart, Optional[NatalChart]]:
        """
        Create natal and optional transit charts.
        
        Args:
            natal_data: Tuple of (name, utc_datetime, latitude, longitude)
            transit_data: Optional tuple of transit data
            
        Returns:
            Tuple of (natal_chart, transit_chart)
        """
        natal_name, natal_dt, natal_lat, natal_lon = natal_data
        
        # Create natal chart
        natal_chart = NatalChart(
            person_name=natal_name,
            dt_utc=natal_dt,
            lat=natal_lat,
            lon=natal_lon,
            orb_config=self.orb_config,
            ephe_path=ephe_path
        )
        
        # Create transit chart if different from natal
        transit_chart = None
        if transit_data:
            transit_name, transit_dt, transit_lat, transit_lon = transit_data
            
            # Only create transit chart if it's different from natal
            if transit_dt != natal_dt or transit_lat != natal_lat or transit_lon != natal_lon:
                transit_chart = NatalChart(
                    person_name=transit_name,
                    dt_utc=transit_dt,
                    lat=transit_lat,
                    lon=transit_lon,
                    orb_config=self.orb_config,
                    ephe_path=ephe_path
                )
        
        return natal_chart, transit_chart
    
    def generate_celestial_bodies_table(self, chart: NatalChart, chart_type: str = "Natal") -> List[List[str]]:
        """Generate celestial bodies table."""
        headers = ["Body", "Type", "Sign", "House", "Dignity"]
        rows = [headers]
        
        for body in chart.bodies_dict.values():
            rows.append([
                body.name,
                body.body_type,
                f"{body.sign.symbol} {body.sign.name}",
                str(body.house),
                body.dignity if body.dignity else "-"
            ])
        
        return rows
    
    def generate_filtered_bodies_table(self, chart: NatalChart, filter_config: BodyFilter, title: str) -> List[List[str]]:
        """Generate filtered celestial bodies table."""
        headers = ["Body", "Type", "Sign", "House", "Dignity"]
        rows = [headers]
        
        filtered_bodies = chart.get_bodies(filter_config)
        for body in filtered_bodies:
            rows.append([
                body.name,
                body.body_type,
                f"{body.sign.symbol} {body.sign.name}",
                str(body.house),
                body.dignity if body.dignity else "-"
            ])
        
        return rows
    
    def generate_aspects_table(self, natal_chart: NatalChart, transit_chart: Optional[NatalChart] = None) -> List[List[str]]:
        """Generate aspects table between natal and transit charts."""
        headers = ["Body1", "Aspect", "Body2", "Phase", "Orb"]
        rows = [headers]
        
        if transit_chart:
            # Calculate aspects between transit and natal
            from nataly import AstroEngine
            engine = AstroEngine(orb_config=self.orb_config)
            aspects = engine.get_aspects(transit_chart.bodies_dict, natal_chart.bodies_dict)
        else:
            # Calculate aspects for natal chart including asteroids
            from nataly import AstroEngine
            engine = AstroEngine(orb_config=self.orb_config)
            aspects = engine.get_aspects(natal_chart.bodies_dict, natal_chart.bodies_dict)
        
        for aspect in aspects:
            phase = "Applying" if aspect.is_applying else "Separating"
            rows.append([
                aspect.body1.name,
                f"{aspect.symbol} {aspect.aspect_type}",
                aspect.body2.name,
                phase,
                aspect.orb_str
            ])
        
        return rows
    
    def generate_aspect_cross_reference_table(self, natal_chart: NatalChart, transit_chart: Optional[NatalChart] = None) -> List[List[str]]:
        """Generate aspect cross reference table."""
        if not transit_chart:
            return [["No transit chart provided"]]
        
        # Get all bodies for headers
        transit_bodies = list(transit_chart.bodies_dict.keys())
        natal_bodies = list(natal_chart.bodies_dict.keys())
        
        # Create headers
        headers = ["Transit"] + transit_bodies
        rows = [headers]
        
        # Calculate aspects
        from nataly import AstroEngine
        engine = AstroEngine(orb_config=self.orb_config)
        aspects = engine.get_aspects(transit_chart.bodies_dict, natal_chart.bodies_dict)
        
        # Create aspect lookup
        aspect_lookup = {}
        for aspect in aspects:
            key = (aspect.body1.name, aspect.body2.name)
            aspect_lookup[key] = f"{aspect.symbol} {aspect.orb_str}"
        
        # Generate rows
        for natal_body in natal_bodies:
            row = [natal_body]
            for transit_body in transit_bodies:
                key = (transit_body, natal_body)
                aspect_info = aspect_lookup.get(key, "-")
                row.append(aspect_info)
            rows.append(row)
        
        return rows
    
    def generate_distribution_table(self, chart: NatalChart, distribution_type: str) -> List[List[str]]:
        """Generate distribution table for elements, modalities, or polarities."""
        headers = ["Category", "Sum", "Bodies"]
        rows = [headers]
        
        if distribution_type == "Element":
            distribution = chart.element_distribution
        elif distribution_type == "Modality":
            distribution = chart.modality_distribution
        elif distribution_type == "Polarity":
            distribution = chart.polarity_distribution
        else:
            return [["Invalid distribution type"]]
        
        for category, data in distribution.items():
            body_names = [body.name for body in data['bodies']]
            rows.append([
                category,
                str(data['count']),
                ", ".join(body_names)
            ])
        
        return rows
    
    def generate_quadrants_table(self, chart: NatalChart) -> List[List[str]]:
        """Generate quadrants table."""
        headers = ["Category", "Sum", "Bodies"]
        rows = [headers]
        
        for quadrant, data in chart.quadrant_distribution.items():
            body_names = [body.name for body in data['bodies']]
            rows.append([
                quadrant,
                str(data['count']),
                ", ".join(body_names)
            ])
        
        return rows
    
    def generate_hemispheres_table(self, chart: NatalChart) -> List[List[str]]:
        """Generate hemispheres table."""
        headers = ["Category", "Sum", "Bodies"]
        rows = [headers]
        
        for hemisphere, data in chart.hemisphere_distribution.items():
            body_names = [body.name for body in data['bodies']]
            rows.append([
                hemisphere,
                str(data['count']),
                ", ".join(body_names)
            ])
        
        return rows
    
    def generate_houses_table(self, chart: NatalChart) -> List[List[str]]:
        """Generate houses table."""
        headers = ["House", "Sign", "Cusp", "Classic Ruler", "Modern Ruler"]
        rows = [headers]
        
        for house in chart.houses:
            classic_ruler = house.classic_ruler.name if house.classic_ruler else "-"
            modern_ruler = house.modern_ruler.name if house.modern_ruler else "-"
            
            rows.append([
                str(house.id),
                f"{house.sign.symbol} {house.sign.name}",
                house.dms,
                classic_ruler,
                modern_ruler
            ])
        
        return rows
    
    def format_table(self, data: List[List[str]]) -> str:
        """Format table data as a string."""
        if not data:
            return "No data available"
        
        # Calculate column widths
        col_widths = []
        for col in range(len(data[0])):
            max_width = max(len(str(row[col])) for row in data)
            col_widths.append(max_width)
        
        # Create separator line
        separator = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"
        
        # Build table
        table_lines = [separator]
        
        for i, row in enumerate(data):
            # Format row
            formatted_row = "|"
            for j, cell in enumerate(row):
                formatted_row += f" {str(cell):<{col_widths[j]}} |"
            table_lines.append(formatted_row)
            
            # Add separator after header
            if i == 0:
                table_lines.append(separator)
        
        table_lines.append(separator)
        
        return "\n".join(table_lines)
    
    def generate_report(self, natal_data: Tuple[str, datetime.datetime, float, float], 
                       transit_data: Optional[Tuple[str, datetime.datetime, float, float]] = None) -> str:
        """
        Generate a comprehensive astrological report.
        
        Args:
            natal_data: Tuple of (name, utc_datetime, latitude, longitude)
            transit_data: Optional tuple of transit data
            
        Returns:
            Formatted report string
        """
        # Create charts
        natal_chart, transit_chart = self.create_charts(natal_data, transit_data)
        
        # Build report
        report_lines = []
        
        # Header
        report_lines.append("=" * 80)
        report_lines.append("ASTROLOGICAL CHART ANALYSIS REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Chart information
        report_lines.append("CHART INFORMATION")
        report_lines.append("-" * 40)
        report_lines.append(f"Natal Chart: {natal_chart.name}")
        report_lines.append(f"Date/Time: {natal_chart.datetime_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        report_lines.append(f"Location: {natal_chart.latitude}°N, {natal_chart.longitude}°E")
        report_lines.append("")
        
        if transit_chart:
            report_lines.append(f"Transit Chart: {transit_chart.name}")
            report_lines.append(f"Date/Time: {transit_chart.datetime_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            report_lines.append(f"Location: {transit_chart.latitude}°N, {transit_chart.longitude}°E")
            report_lines.append("")
        
        # Celestial Bodies
        report_lines.append("CELESTIAL BODIES")
        report_lines.append("-" * 40)
        bodies_table = self.generate_celestial_bodies_table(natal_chart)
        report_lines.append(self.format_table(bodies_table))
        report_lines.append("")
        
        # Filtered bodies examples
        report_lines.append("PLANETS ONLY")
        report_lines.append("-" * 40)
        planet_filter = BodyFilter(include_planets=True, include_luminaries=True, 
                                 include_asteroids=False, include_axes=False, 
                                 include_lunar_nodes=False, include_lilith=False)
        planets_table = self.generate_filtered_bodies_table(natal_chart, planet_filter, "Planets")
        report_lines.append(self.format_table(planets_table))
        report_lines.append("")
        
        # Houses
        report_lines.append("HOUSES")
        report_lines.append("-" * 40)
        houses_table = self.generate_houses_table(natal_chart)
        report_lines.append(self.format_table(houses_table))
        report_lines.append("")
        
        # Aspects
        report_lines.append("ASPECTS")
        report_lines.append("-" * 40)
        aspects_table = self.generate_aspects_table(natal_chart, transit_chart)
        report_lines.append(self.format_table(aspects_table))
        report_lines.append("")
        
        # Distributions
        report_lines.append("ELEMENT DISTRIBUTION")
        report_lines.append("-" * 40)
        element_table = self.generate_distribution_table(natal_chart, "Element")
        report_lines.append(self.format_table(element_table))
        report_lines.append("")
        
        report_lines.append("MODALITY DISTRIBUTION")
        report_lines.append("-" * 40)
        modality_table = self.generate_distribution_table(natal_chart, "Modality")
        report_lines.append(self.format_table(modality_table))
        report_lines.append("")
        
        report_lines.append("POLARITY DISTRIBUTION")
        report_lines.append("-" * 40)
        polarity_table = self.generate_distribution_table(natal_chart, "Polarity")
        report_lines.append(self.format_table(polarity_table))
        report_lines.append("")
        
        # Quadrants and Hemispheres
        report_lines.append("QUADRANT DISTRIBUTION")
        report_lines.append("-" * 40)
        quadrant_table = self.generate_quadrants_table(natal_chart)
        report_lines.append(self.format_table(quadrant_table))
        report_lines.append("")
        
        report_lines.append("HEMISPHERE DISTRIBUTION")
        report_lines.append("-" * 40)
        hemisphere_table = self.generate_hemispheres_table(natal_chart)
        report_lines.append(self.format_table(hemisphere_table))
        report_lines.append("")
        
        # Transit aspects (if available)
        if transit_chart:
            report_lines.append("TRANSIT ASPECTS CROSS REFERENCE")
            report_lines.append("-" * 40)
            cross_ref_table = self.generate_aspect_cross_reference_table(natal_chart, transit_chart)
            report_lines.append(self.format_table(cross_ref_table))
            report_lines.append("")
        
        # Footer
        report_lines.append("=" * 80)
        report_lines.append("Report generated by Nataly Astrological Library")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)


def main():
    """Main function demonstrating the astrological analyzer."""
    # Example birth data (Joe Doe from references.py)
    name = "Joe Doe"
    birth_date = "1990-02-27"
    birth_time = "09:15"  # Local time
    latitude = 38.25  # Izmir, Turkey
    longitude = 27.09
    timezone = "+02:00"
    
    # Initialize analyzer
    analyzer = AstrologicalAnalyzer()
    
    # Parse birth data
    natal_name, natal_dt = analyzer.parse_birth_data(
        name, birth_date, birth_time, latitude, longitude, timezone
    )
    
    # Create natal data tuple
    natal_data = (natal_name, natal_dt, latitude, longitude)
    
    # Optional: Create transit data for current time (use same offset)
    now_local = datetime.datetime.now()
    now_str = now_local.strftime('%Y-%m-%d %H:%M')
    transit_dt = to_utc(now_str, timezone)
    transit_data = ("Current Transit", transit_dt, latitude, longitude)
    
    # Generate report
    print("Generating astrological report...")
    report = analyzer.generate_report(natal_data, transit_data)
    
    # Print report
    print(report)
    
    # Save report to file
    with open("astrological_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\nReport saved to 'astrological_report.txt'")


if __name__ == "__main__":
    main() 