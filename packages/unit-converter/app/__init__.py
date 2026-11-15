import nexapip as tg


class UnitConverter(tg.NexaApp):
    app_id = "unit-converter"
    name = "Unit Converter"
    icon = "assets/icon.png"
    version = "1.0.0"
    description = "Convert common length units from a compact desktop window."

    def build(self, activity, parent, context=None):
        self.activity = activity
        theme = getattr(self, "services", {}).get("theme", {})
        surface = theme.get("surface", 0xFF202630)
        content = theme.get("window_content", 0xFF2B3440)
        text = theme.get("text", 0xFFE8EDF2)
        muted = theme.get("muted", 0xFF9AA8B5)
        self.root = tg.LinearLayout(activity, parent, vertical=True)
        self.root.setdimensions(tg.View.MATCH_PARENT, tg.View.MATCH_PARENT)
        self.root.setbackgroundcolor(surface)

        title = tg.TextView(activity, "length", self.root)
        title.setdimensions(tg.View.MATCH_PARENT, 40)
        title.settextsize(14)
        title.settextcolor(muted)
        title.setgravity(0, 1)
        title.setmargin(10, "left")

        self.value = tg.EditText(activity, "1", self.root, singleline=True,
                                 line=False, inputtype="numberDecimalSigned")
        self.value.setdimensions(tg.View.MATCH_PARENT, 48)
        self.value.setmargin(8, "left")
        self.value.setmargin(8, "right")
        self.value.setbackgroundcolor(content)
        self.value.settextcolor(text)
        self.value.settextsize(18)

        self.result = tg.TextView(activity, "1 meter", self.root)
        self.result.setdimensions(tg.View.MATCH_PARENT, 56)
        self.result.settextsize(22)
        self.result.settextcolor(text)
        self.result.setgravity(1, 1)

        self.actions = {}
        units = (("km", 0.001), ("cm", 100), ("mm", 1000), ("ft", 3.280839895))
        row = tg.LinearLayout(activity, self.root, vertical=False)
        row.setdimensions(tg.View.MATCH_PARENT, 48)
        for label, multiplier in units:
            button = tg.TextView(activity, label, row)
            button.setdimensions(0, 42)
            button.setlinearlayoutparams(1)
            button.setmargin(3, "left")
            button.setmargin(3, "right")
            button.setbackgroundcolor(content)
            button.settextcolor(text)
            button.settextsize(14)
            button.setgravity(1, 1)
            button.sendclickevent(True)
            self.actions[button.id] = (label, multiplier)
        return self

    def handle_event(self, event):
        if event.type != tg.Event.click or event.id not in self.actions:
            return False
        unit, multiplier = self.actions[event.id]
        try:
            value = float(self.value.gettext())
            if not __import__("math").isfinite(value):
                raise ValueError
        except (TypeError, ValueError):
            self.result.settext("enter a valid number")
            return True
        converted = value * multiplier
        self.result.settext(f"{converted:.8g} {unit}")
        return True


APP = UnitConverter()
