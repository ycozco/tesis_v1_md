from dbfread import DBF

def test_dbf():
    dbf_path = 'data/sunat/x23290326.DBF'
    print("Reading", dbf_path)
    dbf = DBF(dbf_path, load=False)

    target_hs = {
        810400000: 'Blueberry',
        806100000: 'Grape',
        804400000: 'Avocado',
        709200000: 'Asparagus',
        1801001900: 'Cocoa'
    }

    counts = {k: 0 for k in target_hs}
    matching_records = []

    for record in dbf:
        partida = record.get('PART_NANDI')
        try:
            part_int = int(partida)
        except:
            continue
        
        if part_int in target_hs:
            counts[part_int] += 1
            matching_records.append((target_hs[part_int], record.copy()))

    print('Matching counts:')
    for k, v in counts.items():
        print(f'  {target_hs[k]} ({k}): {v} records')

    print('\nSample matching records:')
    for crop, rec in matching_records[:10]:
        print(f"Crop: {crop:10} | RUC: {rec.get('NDOC'):11} | Name: {rec.get('DNOMBRE')[:30]:30} | FOB: {rec.get('VFOBSERDOL'):10.2f} | PesoNet: {rec.get('VPESNET'):10.2f} | Dest: {rec.get('CPAIDES'):2} | Date: {rec.get('FNUM')}")

if __name__ == '__main__':
    test_dbf()
