extends Control

## Placeholder script that mirrors how the dashboard would request
## project data from the simulation kernel once the API is wired up.
## For now, we show static mock entries that match the research focus
## of the first playable prototype.

@export var mock_projects := [
    {
        "name": "Project Helios",
        "type": "Chatbot",
        "status": "Planning",
        "eta_days": 45,
    },
    {
        "name": "Aurora QA",
        "type": "Tooling",
        "status": "Training",
        "eta_days": 12,
    },
    {
        "name": "Muse Support",
        "type": "Chatbot",
        "status": "Released",
        "eta_days": 0,
    },
]

var _list_container: VBoxContainer

func _ready() -> void:
    _ensure_list_container()
    _render_mock_rows()

func _ensure_list_container() -> void:
    if _list_container:
        return
    _list_container = VBoxContainer.new()
    _list_container.name = "MockList"
    _list_container.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    _list_container.size_flags_vertical = Control.SIZE_EXPAND_FILL
    _list_container.custom_minimum_size = Vector2(0, 200)
    add_child(_list_container)

func _render_mock_rows() -> void:
    _clear_children(_list_container)
    for project in mock_projects:
        var panel := PanelContainer.new()
        panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        panel.add_theme_constant_override("margin_top", 8)
        panel.add_theme_constant_override("margin_bottom", 8)
        panel.add_theme_constant_override("margin_left", 12)
        panel.add_theme_constant_override("margin_right", 12)

        var hbox := HBoxContainer.new()
        hbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        hbox.custom_minimum_size = Vector2(0, 48)

        var name_label := Label.new()
        name_label.text = "%s (%s)" % [project.get("name", "Unnamed"), project.get("type", "-")]
        name_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT

        var status_label := Label.new()
        status_label.text = project.get("status", "?")
        status_label.size_flags_horizontal = Control.SIZE_FILL
        status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER

        var eta_label := Label.new()
        eta_label.text = _format_eta(project.get("eta_days", 0))
        eta_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT

        hbox.add_child(name_label)
        hbox.add_child(status_label)
        hbox.add_child(eta_label)

        panel.add_child(hbox)
        _list_container.add_child(panel)

func _format_eta(days: int) -> String:
    if days <= 0:
        return "Live"
    return "%d d" % days

func _clear_children(container: Node) -> void:
    for child in container.get_children():
        child.queue_free()
