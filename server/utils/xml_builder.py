import xml.etree.ElementTree as ET


def dumps(struct):
    root = ET.Element('root')
    build_tree(root, struct)

    return ET.tostring(root)


def build_tree(parent: ET.Element, struct):
    if type(struct) in [int, float, str, bool] or struct is None:
        el = ET.SubElement(parent, 'element')
        el.text = str(struct)

        return

    if type(struct) in [list, set, tuple]:
        seq_node = ET.SubElement(parent, 'sequence')

        for el in struct:
            item_node = ET.SubElement(seq_node, 'item')
            build_tree(item_node, el)

        return

    if isinstance(struct, dict):
        dict_node = ET.SubElement(parent, 'dict')

        for k, v in struct.items():
            pair_node = ET.SubElement(dict_node, 'pair')

            key_node = ET.SubElement(pair_node, 'key')
            build_tree(key_node, k)

            value_node = ET.SubElement(pair_node, 'value')
            build_tree(value_node, v)

        return
