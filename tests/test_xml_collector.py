import pytest
import logging

import xml.etree.ElementTree as ET

#from pytpy.xml_obj import Symbol, DataType
from pytpy import Symbol, DataType, SubItem
from pytpy.xml_obj import BaseElement

from pytpy import TmcFile
from pytpy.xml_collector import ElementCollector

from collections import defaultdict

logger = logging.getLogger(__name__)



def test_ElementCollector_instantiation(generic_tmc_root):
    try:
        col = ElementCollector()
    except:
        pytest.fail(
            "Instantiation of XmlObjCollector should not generate errors"
        )


def test_ElementCollector_add(generic_tmc_root):
    root = generic_tmc_root
    iterator = DataType(root.find("./DataTypes/DataType/[Name='iterator']"))
    version = DataType(root.find("./DataTypes/DataType/[Name='VERSION']"))
    col = ElementCollector()
    col.add(iterator)
    col.add(version)
    assert 'iterator' in col
    assert 'VERSION' in col
    
    col.add(version)
    assert len(col) == 2
    
    assert col['iterator'] == iterator
    assert col['VERSION'] == version 


def test_ElementCollector_registered(generic_tmc_root):
    root = generic_tmc_root
    iterator = DataType(root.find("./DataTypes/DataType/[Name='iterator']"))
    iterator.registered_pragmas.append("iterator attr")
    version = DataType(root.find("./DataTypes/DataType/[Name='VERSION']"))
    col = ElementCollector()
    col.add(iterator)
    col.add(version)

    print(col['iterator'].pragmas)
    print(col['VERSION'].pragmas)
    assert col['iterator'].pragmas == {'iterator attr':['42']}
    assert col.registered == {'iterator':iterator}


def test_TmcFile_instantiation(generic_tmc_path,generic_tmc_root):
    try:
        tmc = TmcFile(generic_tmc_path)
    except:
        pytest.fail("Instantiation of TmcFile should not generate errors")


def test_TmcFile_isolate_Symbols(generic_tmc_path):
    tmc = TmcFile(generic_tmc_path)
    tmc.isolate_Symbols()

    assert "MAIN.ulimit" in tmc.all_Symbols
    assert "MAIN.count" in tmc.all_Symbols
    assert "MAIN.NEW_VAR" in tmc.all_Symbols
    assert "MAIN.test_iterator" in tmc.all_Symbols
    assert "Constants.RuntimeVersion" in tmc.all_Symbols

    assert len(tmc.all_Symbols) == 18


def test_TmcFile_isolate_DataTypes(generic_tmc_path):
    tmc = TmcFile(generic_tmc_path)
    tmc.isolate_DataTypes()

    assert "iterator" in tmc.all_DataTypes
    assert "VERSION" in tmc.all_DataTypes

    assert len(tmc.all_DataTypes) == 7


def test_TmcFile_isolate_SubItems(generic_tmc_path):
    tmc = TmcFile(generic_tmc_path)
    tmc.isolate_DataTypes(process_subitems=False)
    tmc.isolate_SubItems('iterator')

    assert 'increment' in tmc.all_SubItems['iterator']
    assert 'out' in tmc.all_SubItems['iterator']
    assert 'value' in tmc.all_SubItems['iterator']
    assert 'lim' in tmc.all_SubItems['iterator']
   
    assert len(tmc.all_SubItems['iterator']) == 4




def test_TmcFile_isolate_all(generic_tmc_path):
    tmc = TmcFile(generic_tmc_path)
    tmc.isolate_all()
    
    assert "MAIN.ulimit" in tmc.all_Symbols
    assert "MAIN.count" in tmc.all_Symbols
    assert "MAIN.NEW_VAR" in tmc.all_Symbols
    assert "MAIN.test_iterator" in tmc.all_Symbols
    assert "Constants.RuntimeVersion" in tmc.all_Symbols

    assert len(tmc.all_Symbols) == 18


    assert "iterator" in tmc.all_DataTypes
    assert "VERSION" in tmc.all_DataTypes

    assert len(tmc.all_DataTypes) == 7

    '''
    for x in tmc.all_DataTypes:
        print("\t",x,"  ", len(tmc.all_DataTypes[x].children))
        for y in tmc.all_DataTypes[x].children:
            print("\t\t",y)
    '''

    assert 'increment' in tmc.all_SubItems['iterator']
    assert 'out' in tmc.all_SubItems['iterator']
    assert 'value' in tmc.all_SubItems['iterator']
    assert 'lim' in tmc.all_SubItems['iterator']
   
    assert len(tmc.all_SubItems['iterator']) == 4



