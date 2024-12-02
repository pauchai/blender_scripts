import bpy
import json
from bpy_extras.io_utils import ExportHelper

bl_info = {
    "name": "Text Block Properties Exporter",
    "blender": (2, 80, 0),  # Минимальная версия Blender
    "category": "Sequencer",
    "description": "Export properties of text blocks to a JSON file",
    "author": "Ваше имя",
    "version": (1, 0),
    "support": "COMMUNITY",
    "tracker_url": "",  # Ссылка на трекер задач (если есть)
    "wiki_url": "",     # Ссылка на документацию (если есть)
}

def list_sequencer_channels():
    # Получаем доступ к секвенсеру
    sequencer = bpy.context.scene.sequence_editor

    # Проверяем, есть ли секвенсер
    if sequencer:
        # Получаем количество каналов
        max_channels = len(sequencer.channels)
        
        print(f"Количество каналов: {max_channels}")
        
        # Выводим информацию о каждом канале
        for channel in sequencer.channels:
            print(f"Имя канала: {channel.name}")
    else:
        print("Секвенсер не найден.")



# Функция для получения свойств всех текстовых блоков в JSON
def get_text_blocks_properties():
    text_data = []
    for strip in bpy.context.scene.sequence_editor.sequences_all:
        if strip.type == 'TEXT':
            text_data.append({
                "name": strip.name,
                "channel": strip.channel,
                "frame_start": strip.frame_start,
                "frame_end": strip.frame_final_end,
                "text": strip.text
            })
    return json.dumps(text_data, indent=4)

# Оператор для экспорта JSON с диалоговым окном
class SEQUENCER_OT_export_text_props(bpy.types.Operator, ExportHelper):
    bl_idname = "sequencer.export_text_props"
    bl_label = "Export Text Block Properties"
    bl_description = "Export text block properties to a JSON file"

    # Настройки фильтра файлов для диалога
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
    )

    def execute(self, context):
        # Получаем JSON строку со свойствами текстовых блоков
        text_json = get_text_blocks_properties()
        
        # Сохраняем JSON в файл
        with open(self.filepath, 'w') as file:
            file.write(text_json)
        
        self.report({'INFO'}, f"Text properties saved to {self.filepath}")
        return {'FINISHED'}

# Панель в Video Sequencer
class SEQUENCER_PT_text_block_props_panel(bpy.types.Panel):
    bl_label = "Text Block Properties"
    bl_idname = "SEQUENCER_PT_text_block_props_panel"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Text Properties'

    def draw(self, context):
        layout = self.layout
        layout.operator("sequencer.export_text_props", text="Export Text Properties")

# Регистрация классов
def register():
    bpy.utils.register_class(SEQUENCER_OT_export_text_props)
    bpy.utils.register_class(SEQUENCER_PT_text_block_props_panel)

def unregister():
    bpy.utils.unregister_class(SEQUENCER_PT_text_block_props_panel)
    bpy.utils.unregister_class(SEQUENCER_OT_export_text_props)

# Проверка на запуск в качестве аддона
if __name__ == "__main__":
    register()
