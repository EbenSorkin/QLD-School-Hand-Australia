import yaml

yaml.Dumper.ignore_aliases = lambda *args : True

features = {
    "ss01": "Precursive",
    "ss02": "Outline",
    "ss03": "Cursive",
    "ss04": "Outline Starters",
    "ss05": "Outline Arrows",
    "ss06": "Dotted"
}
STATICS = {
    "Regular": 400,
    "Medium": 500,
    "SemiBold": 600,
    "Bold": 700,
}

fix = { "operation": "fix" }
subset = { "operation": "hbsubset", }

def varfont_path(suffix=None):
    if suffix:
        return f"../fonts/variable/QLDSchoolHand{suffix}[wght].ttf"
    else:
        return "../fonts/variable/QLDSchoolHand[wght].ttf"
    
def static_path(suffix, style):
    return f"../fonts/static/QLDSchoolHand{suffix}-{style}.ttf"

base_steps = [
    { "source": "QLDSchoolHand.glyphs"},
    { "operation": "buildVariable" ,
      "fontmake_args": '--filter ... --filter FlattenComponentsFilter --filter DecomposeTransformedComponentsFilter '},
    { "operation": "buildStat"},
]

guideline_steps = [
    { "source": "QLDSchoolHand.glyphs"},
    { "operation": "exec", "exe": "python3 ../scripts/add-guidelines.py", "args": "-o QLDSchoolHand-Guidelines.glyphs --overlap 200 QLDSchoolHand.glyphs"},
    { "source": "QLDSchoolHand-Guidelines.glyphs"},
    { "operation": "buildVariable",
     "fontmake_args": '--filter ... --filter FlattenComponentsFilter --filter DecomposeTransformedComponentsFilter '},
    { "operation": "buildStat"},
]

config = {
    "axisOrder": ["wght"],
    "familyName": "QLD School Hand",
    "sources": ["QLDSchoolHand.glyphs"],
    "recipe": {
        varfont_path(): base_steps + [fix],
        varfont_path("Guidelines"): guideline_steps + [fix]
    }
}

for feature, name in features.items():
    tidyname = name.replace(" ", "")
    config["recipe"][varfont_path(tidyname)] = base_steps + [
        { "operation": "featureFreeze", "args": "-f "+feature },
        { "operation": "rename", "name": "QLD School Hand "+name },
        subset, fix
    ]

    config["recipe"][varfont_path(tidyname+'-Guidelines')] = guideline_steps + [
        { "operation": "featureFreeze", "args": "-f "+feature },
        { "operation": "rename", "name": "QLD School Hand "+name+" Guidelines" },
        subset, fix
    ]

    # Statics!
    for style, wght in STATICS.items():
        config["recipe"][static_path(tidyname, style)] = base_steps + [
            { "operation": "featureFreeze", "args": "-f "+feature },
            { "operation": "rename", "name": "QLD School Hand "+name },
            {
                            "operation": "subspace",
                            "axes": f"wght={wght}",
                            "other_args": "--update-name-table"
            },
            { "operation": "autohint"},
            subset,
            {"postprocess": "fix", "fixargs": "--include-source-fixes"}
        ]

with open("sources/config.yaml", "w") as file:
    yaml.dump(config, file, sort_keys=False, default_flow_style = False)
