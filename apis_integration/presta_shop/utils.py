import xml.etree.ElementTree
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString


def create_prestashop_base_xml():
    return Element("prestashop")


def add_seo_xml_sub_elements(parent_element: Element, data: dict):
    meta_title = SubElement(parent_element, "meta_title")
    language = SubElement(meta_title, "language", id="1")
    language.text = data["meta_title"]
    meta_description = SubElement(parent_element, "meta_description")
    language = SubElement(meta_description, "language", id="1")
    language.text = data["meta_description"]
    meta_keywords = SubElement(parent_element, "meta_keywords")
    language = SubElement(meta_keywords, "language", id="1")
    language.text = data["meta_keywords"]
    return parent_element


def create_english_sub_element(
    parent_element: Element, element_name: str, element_value: str
):
    element = SubElement(parent_element, element_name)
    language = SubElement(element, "language", id="1")
    language.text = element_value
    return parent_element


def prettify_xml(element: Element):
    tree = xml.etree.ElementTree.ElementTree(element)
    tree.write("test.xml")
    return parseString(tostring(element)).toprettyxml()
