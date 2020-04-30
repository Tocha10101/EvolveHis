from optimization import Optimization
from csv import DictReader, DictWriter

optimization = None

def test_drive():
    with open('calls_metadata_2d.csv', 'r') as csv_read, open('result_data.csv', 'w', newline='') as csv_write:
        csv_reader = DictReader(csv_read, delimiter=',')
        fieldnames = [item for item in csv_reader.fieldnames]
        fieldnames.remove('Function num')
        fieldnames.append('Best')
        fieldnames.append('Timestamp')
        fieldnames.append('Generation of change')
        csv_writer = DictWriter(csv_write, fieldnames=fieldnames)
        csv_writer.writeheader()
        for row in csv_reader:
            metadata = {
                'dim': int(row['Dim']),
                'mu': int(row['Mu']),
                'lambda': int(row['Lambda']),
                'function_num': int(row['Function num']),
                'heur_available': bool(row['Heuristic']),
                'generation_limit': int(row['Generations']),
                'starting_generation': 0
            }
            for i in range(10):
                optimization = Optimization(metadata)
                best, timestamp, change_gen = optimization.main()
                csv_writer.writerow({
                    'Function name': row['Function name'],
                    'Mu': metadata['mu'],
                    'Lambda': metadata['lambda'],
                    'Generations': metadata['generation_limit'],
                    'Heuristic': metadata['heur_available'],
                    'Dim': metadata['dim'],    
                    'Best': str(best.describe()),
                    'Timestamp': timestamp,
                    'Generation of change': change_gen
                })


test_drive()
