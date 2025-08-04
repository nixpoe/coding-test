import unittest
import os
import tempfile
import pandas as pd
import sys
from unittest.mock import patch
from io import StringIO

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import calculator
from stock_data_cli.src.loader.base_loader import BaseLoader
from stock_data_cli.src.loader.base_saver import BaseSaver
from stock_data_cli.src.loader.csv_loader import CsvLoader
from stock_data_cli.src.loader.json_loader import JsonLoader
from stock_data_cli.src.loader.parquet_loader import ParquetLoader
from stock_data_cli.src.loader.csv_saver import CsvSaver
from stock_data_cli.src.loader.json_saver import JsonSaver
from stock_data_cli.src.loader.parquet_saver import ParquetSaver
from stock_data_cli.src.returns.forward_adjusted import ForwardAdjusted
from stock_data_cli.src.returns.backward_adjusted import BackwardAdjusted


class TestStrategyPattern(unittest.TestCase):
    """Test the Strategy pattern implementation for loaders and savers"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_data = pd.DataFrame({
            'unadjusted_close': [100.0, 102.0, 101.0],
            'ticker_symbol': ['TEST', 'TEST', 'TEST'],
            'datetime': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
            'split': [1.0, 1.0, 2.0],
            'dividend': [0.0, 1.0, 0.0]
        })
    
    def test_loader_supported_extensions(self):
        """Test that each loader reports correct supported extensions"""
        csv_loader = CsvLoader("dummy.csv")
        json_loader = JsonLoader("dummy.json")
        parquet_loader = ParquetLoader("dummy.parquet")
        
        self.assertEqual(csv_loader.supported_extensions, ['.csv'])
        self.assertEqual(json_loader.supported_extensions, ['.json'])
        self.assertEqual(parquet_loader.supported_extensions, ['.parquet', '.pq'])
    
    def test_saver_supported_extensions(self):
        """Test that each saver reports correct supported extensions"""
        csv_saver = CsvSaver("dummy.csv")
        json_saver = JsonSaver("dummy.json")
        parquet_saver = ParquetSaver("dummy.parquet")
        
        self.assertEqual(csv_saver.supported_extensions, ['.csv'])
        self.assertEqual(json_saver.supported_extensions, ['.json'])
        self.assertEqual(parquet_saver.supported_extensions, ['.parquet', '.pq'])
    
    def test_loader_can_handle(self):
        """Test the can_handle method for loaders"""
        csv_loader = CsvLoader("dummy.csv")
        
        # Test correct extension
        self.assertTrue(csv_loader.can_handle('.csv'))
        self.assertTrue(csv_loader.can_handle('.CSV'))  # Case insensitive
        
        # Test incorrect extension
        self.assertFalse(csv_loader.can_handle('.json'))
        self.assertFalse(csv_loader.can_handle('.parquet'))
        self.assertFalse(csv_loader.can_handle('.pq'))
    
    def test_saver_can_handle(self):
        """Test the can_handle method for savers"""
        json_saver = JsonSaver("dummy.json")
        
        # Test correct extension
        self.assertTrue(json_saver.can_handle('.json'))
        self.assertTrue(json_saver.can_handle('.JSON'))  # Case insensitive
        
        # Test incorrect extension
        self.assertFalse(json_saver.can_handle('.csv'))
        self.assertFalse(json_saver.can_handle('.parquet'))
        self.assertFalse(json_saver.can_handle('.pq'))
    
    def test_loader_factory_method(self):
        """Test the factory method for loaders"""
        # Test CSV
        loader = BaseLoader.get_loader_for_file("test.csv")
        self.assertIsInstance(loader, CsvLoader)
        
        # Test JSON
        loader = BaseLoader.get_loader_for_file("test.json")
        self.assertIsInstance(loader, JsonLoader)
        
        # Test Parquet
        loader = BaseLoader.get_loader_for_file("test.parquet")
        self.assertIsInstance(loader, ParquetLoader)
        
        # Test unsupported format
        with self.assertRaises(ValueError) as context:
            BaseLoader.get_loader_for_file("test.xlsx")
        self.assertIn("No loader found for file extension", str(context.exception))
    
    def test_saver_factory_method(self):
        """Test the factory method for savers"""
        # Test CSV
        saver = BaseSaver.get_saver_for_file("test.csv")
        self.assertIsInstance(saver, CsvSaver)
        
        # Test JSON
        saver = BaseSaver.get_saver_for_file("test.json")
        self.assertIsInstance(saver, JsonSaver)
        
        # Test Parquet
        saver = BaseSaver.get_saver_for_file("test.parquet")
        self.assertIsInstance(saver, ParquetSaver)
        
        # Test unsupported format
        with self.assertRaises(ValueError) as context:
            BaseSaver.get_saver_for_file("test.xlsx")
        self.assertIn("No saver found for file extension", str(context.exception))


class TestFileOperations(unittest.TestCase):
    """Test actual file loading and saving operations"""
    
    def setUp(self):
        """Set up test data and temporary directory"""
        self.sample_data = pd.DataFrame({
            'unadjusted_close': [100.0, 102.0, 101.0],
            'ticker_symbol': ['TEST', 'TEST', 'TEST'],
            'datetime': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
            'split': [1.0, 1.0, 2.0],
            'dividend': [0.0, 1.0, 0.0]
        })
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_csv_round_trip(self):
        """Test saving and loading CSV files"""
        csv_path = os.path.join(self.temp_dir, "test.csv")
        
        # Save data
        saver = CsvSaver(csv_path)
        saver.save(self.sample_data)
        
        # Load data
        loader = CsvLoader(csv_path)
        loaded_data = loader.load_data()
        
        # Verify data integrity
        self.assertEqual(len(loaded_data), 3)
        self.assertListEqual(list(loaded_data.columns), 
                           ['unadjusted_close', 'ticker_symbol', 'datetime', 'split', 'dividend'])
        self.assertEqual(loaded_data['ticker_symbol'].iloc[0], 'TEST')
    
    def test_json_round_trip(self):
        """Test saving and loading JSON files"""
        json_path = os.path.join(self.temp_dir, "test.json")
        
        # Save data
        saver = JsonSaver(json_path)
        saver.save(self.sample_data)
        
        # Load data
        loader = JsonLoader(json_path)
        loaded_data = loader.load_data()
        
        # Verify data integrity
        self.assertEqual(len(loaded_data), 3)
        self.assertListEqual(list(loaded_data.columns), 
                           ['unadjusted_close', 'ticker_symbol', 'datetime', 'split', 'dividend'])
    
    def test_parquet_round_trip(self):
        """Test saving and loading Parquet files"""
        parquet_path = os.path.join(self.temp_dir, "test.parquet")
        
        # Save data
        saver = ParquetSaver(parquet_path)
        saver.save(self.sample_data)
        
        # Load data
        loader = ParquetLoader(parquet_path)
        loaded_data = loader.load_data()
        
        # Verify data integrity
        self.assertEqual(len(loaded_data), 3)
        self.assertListEqual(list(loaded_data.columns), 
                           ['unadjusted_close', 'ticker_symbol', 'datetime', 'split', 'dividend'])


class TestCalculationMethods(unittest.TestCase):
    """Test the forward and backward adjustment calculations"""
    
    def setUp(self):
        """Set up test data with known splits and dividends"""
        self.test_data = pd.DataFrame({
            'unadjusted_close': [100.0, 105.0, 110.0, 115.0],
            'ticker_symbol': ['TEST', 'TEST', 'TEST', 'TEST'],
            'datetime': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']),
            'split': [1.0, 1.0, 2.0, 1.0],  # 2:1 split on day 3
            'dividend': [0.0, 1.0, 0.0, 0.0]  # $1 dividend on day 2
        })
    
    def test_forward_adjusted_calculation(self):
        """Test forward adjustment calculation"""
        forward_adj = ForwardAdjusted(self.test_data)
        result = forward_adj.forward_adj()

        expected = [100.0, 105, 111.05, 232.19] # rucno izracunato

        self.assertTrue(
            all(abs(a - b) < 0.000001 for a, b in zip(result['forward_adj_close'], expected)),
            f"Expected {expected}, got {result['forward_adj_close'].tolist()}"
        )
    
    def test_backward_adjusted_calculation(self):
        """Test backward adjustment calculation"""
        backward_adj = BackwardAdjusted(self.test_data)
        result = backward_adj.backward_adj()

        expected = [49.05, 52.5, 110, 115.0]  # rucno izracunato
        
        self.assertTrue(
            all(abs(a - b) < 0.000001 for a, b in zip(result['backward_adj_close'], expected)),
            f"Expected {expected}, got {result['backward_adj_close'].tolist()}"
        )


class TestCalculatorMain(unittest.TestCase):
    """Test the main calculator functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test data file
        test_data = pd.DataFrame({
            'unadjusted_close': [100.0, 102.0, 101.0, 105.0],
            'ticker_symbol': ['TEST', 'TEST', 'TEST', 'TEST'],
            'datetime': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']),
            'split': [1.0, 1.0, 2.0, 1.0],
            'dividend': [0.0, 1.0, 0.0, 0.0]
        })
        
        # Save test data in different formats
        self.csv_file = os.path.join(self.temp_dir, "test_data.csv")
        self.json_file = os.path.join(self.temp_dir, "test_data.json")
        self.parquet_file = os.path.join(self.temp_dir, "test_data.parquet")
        
        test_data.to_csv(self.csv_file, index=False)
        test_data.to_json(self.json_file, orient='records', lines=True)
        test_data.to_parquet(self.parquet_file, index=False)
    
    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('sys.argv')
    def test_calculator_with_csv_input(self, mock_argv):
        """Test calculator with CSV input"""
        output_file = os.path.join(self.temp_dir, "output.csv")
        mock_argv.__getitem__.side_effect = lambda i: [
            'calculator.py', '--input', self.csv_file, '--output', output_file, '--mode', 'forward'
        ][i]
        mock_argv.__len__.return_value = 7
        
        # Capture stdout to check for errors
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            calculator.main()
            
            # Check that output file was created
            self.assertTrue(os.path.exists(output_file))
            
            # Load and verify output
            result = pd.read_csv(output_file)
            self.assertIn('forward_adj_close', result.columns)
            self.assertEqual(len(result), 4)
            
        except SystemExit as e:
            self.fail(f"Calculator exited with error: {e}")
        finally:
            sys.stdout = old_stdout
    
    @patch('sys.argv')
    def test_calculator_with_nonexistent_file(self, mock_argv):
        """Test calculator with non-existent input file"""
        mock_argv.__getitem__.side_effect = lambda i: [
            'calculator.py', '--input', 'nonexistent.csv', '--mode', 'forward'
        ][i]
        mock_argv.__len__.return_value = 5
        
        with self.assertRaises(SystemExit) as context:
            calculator.main()
        
        self.assertEqual(context.exception.code, 1)
    
    @patch('sys.argv')
    def test_calculator_with_unsupported_format(self, mock_argv):
        """Test calculator with unsupported file format"""
        unsupported_file = os.path.join(self.temp_dir, "test.xlsx")
        with open(unsupported_file, 'w') as f:
            f.write("dummy content")
        
        mock_argv.__getitem__.side_effect = lambda i: [
            'calculator.py', '--input', unsupported_file, '--mode', 'forward'
        ][i]
        mock_argv.__len__.return_value = 5
        
        with self.assertRaises(SystemExit) as context:
            calculator.main()
        
        self.assertEqual(context.exception.code, 1)


class TestIntegration(unittest.TestCase):
    """Integration tests using real data"""
    
    def test_with_actual_data_file(self):
        """Test with the actual data.parquet file if it exists"""
        data_file = os.path.join(os.path.dirname(__file__), 'data', 'data.parquet')
        
        if os.path.exists(data_file):
            # Test that we can load the file using our Strategy pattern
            loader = BaseLoader.get_loader_for_file(data_file)
            self.assertIsInstance(loader, ParquetLoader)
            
            # Test that we can load the data
            data = loader.load_data()
            self.assertIsInstance(data, pd.DataFrame)
            
            # Test that it has required columns
            required_columns = ['unadjusted_close', 'ticker_symbol', 'datetime', 'split', 'dividend']
            for col in required_columns:
                self.assertIn(col, data.columns)
            
            # Test calculations work
            forward_adj = ForwardAdjusted(data)
            result = forward_adj.forward_adj()
            self.assertIn('forward_adj_close', result.columns)
        else:
            self.skipTest("data.parquet file not found")


if __name__ == '__main__':
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestStrategyPattern))
    suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculationMethods))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculatorMain))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")

