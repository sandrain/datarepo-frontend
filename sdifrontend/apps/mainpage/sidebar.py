from django import template

register = template.Library()

class SidebarMenu:
    def __init__(self):
        self.nav_elements = [
            {
                'name': "Data Subject",
                'items': [
                    {'name': "Coal, Lignite, and Peat"},
                    {'name': "Petroleum"},
                    {'name': "Natural Gas"},
                    {'name': "Oil Shales And Tar Sands"},
                    {'name': "Isotope And Radiation Sources"},
                    {'name': "Hydrogen"},
                    {'name': "Biomass Fuels"},
                    {'name': "Synthetic Fuels"},
                    {'name': "Nuclear Fuel Cycle And Fuel Materials"},
                    {'name': "Management Of Radioactive And Non-Radioactive Wastes From Nuclear Facilities"},
                    {'name': "Hydro Energy"},
                    {'name': "Solar Energy"},
                    {'name': "Geothermal Energy"},
                    {'name': "Tidal And Wave Power"},
                    {'name': "Wind Energy"},
                    {'name': "Fossil-Fueled Power Plants"},
                    {'name': "Specific Nuclear Reactors And Associated Plants"},
                    {'name': "General Studies Of Nuclear Reactors"},
                    {'name': "Power Transmission And Distribution"},
                    {'name': "Energy Storage"},
                    {'name': "Energy Planning, Policy, And Economy"},
                    {'name': "Direct Energy Conversion"},
                    {'name': "Energy Conservation, Consumption, And Utilization"},
                    {'name': "Advanced Propulsion Systems"},
                    {'name': "Materials Science"},
                    {'name': "Inorganic, Organic, Physical, And Analytical Chemistry"},
                    {'name': "Radiation Chemistry, Radiochemistry, And Nuclear Chemistry"},
                    {'name': "Engineering"},
                    {'name': "Particle Accelerators"},
                    {'name': "Military Technology, Weaponry, And National Defense"},
                    {'name': "Instrumentation Related To Nuclear Science And Technology"},
                    {'name': "Other Instrumentation"},
                    {'name': "Environmental Sciences"},
                    {'name': "Geosciences"},
                    {'name': "Basic Biological Sciences"},
                    {'name': "Applied Life Sciences"},
                    {'name': "Radiation Protection And Dosimetry"},
                    {'name': "Radiology And Nuclear Medicine"},
                    {'name': "Radiation, Thermal, And Other Environ. Pollutant Effects On Living Orgs. And Biol. Mat."},
                    {'name': "Plasma Physics And Fusion Technology"},
                    {'name': "Classical And Quantum Mechanics, General Physics"},
                    {'name': "Physics Of Elementary Particles And Fields"},
                    {'name': "Nuclear Physics And Radiation Physics"},
                    {'name': "Atomic And Molecular Physics"},
                    {'name': "Condensed Matter Physics, Superconductivity And Superfluidity"},
                    {'name': "Nanoscience And Nanotechnology"},
                    {'name': "Astronomy And Astrophysics"},
                    {'name': "Knowledge Management And Preservation"},
                    {'name': "Mathematics And Computing"},
                    {'name': "Nuclear Disarmament, Safeguards, And Physical Protection"},
                    {'name': "General And Miscellaneous"}
                ]
            }, {
                'name': "Data Type",
                'items': [
                    {'name': "Animations/Simulations"},
                    {'name': "Genome/Genetic Data"},
                    {'name': "Interactive Data Map"},
                    {'name': "Numeric Data"},
                    {'name': "Still Images/Photos"},
                    {'name': "Figures/Plots"},
                    {'name': "Specialized Mix"},
                    {'name': "Multimedia"},
                    {'name': "General (Other)"}
                ]
            }
        ]


@register.simple_tag(takes_context=True)
def get_sidebar_items(context, **kwargs):
    sb = SidebarMenu()
    return sb.nav_elements


@register.simple_tag(takes_context=True)
def get_ds_types(context, **kwargs):
    sb = SidebarMenu()
    items = sb.nav_elements[1]['items']
    options = []
    for item in items:
        o = ('0', item['name'])
        options.append(o)
    return options


@register.simple_tag(takes_context=True)
def get_ds_subjects(context, **kwargs):
    sb = SidebarMenu()
    items = sb.nav_elements[0]['items']

    options = []
    for item in items:
        o = ("{}".format(items.index(item)), item['name'])
        options.append(o)
    return options
