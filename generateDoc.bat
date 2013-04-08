del Documentation\*.html

python -m pydoc -w EveCentral
python -m pydoc -w EveDB
python -m pydoc -w EveInvBlueprintType
python -m pydoc -w EveInvCategory
python -m pydoc -w EveInvGroup
python -m pydoc -w EveInvType
python -m pydoc -w EveMapRegion
python -m pydoc -w EveMapSolarSystem

del *.pyc
move *.html Documentation