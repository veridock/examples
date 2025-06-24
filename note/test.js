/**
 * Unit tests for Notes PWA.SVG Application
 */

// Mock localStorage for testing
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => {
      store[key] = value.toString();
    },
    clear: () => {
      store = {};
    },
    removeItem: (key) => {
      delete store[key];
    }
  };
})();

// Mock document for testing
document = {
  getElementById: jest.fn().mockImplementation((id) => ({
    value: '',
    addEventListener: jest.fn(),
  })),
  querySelector: jest.fn().mockImplementation(() => ({
    textContent: '',
  })),
};

// Import the functions to test
const { saveNote, loadNote } = require('./note.pwa.svg');

describe('Notes Application', () => {
  beforeEach(() => {
    // Clear all mocks and localStorage before each test
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('saveNote', () => {
    it('should save note to localStorage', () => {
      const testText = 'Test note content';
      saveNote(testText);
      expect(localStorage.setItem).toHaveBeenCalledWith('note', testText);
    });
  });

  describe('loadNote', () => {
    it('should load note from localStorage', () => {
      const testText = 'Test note content';
      localStorage.setItem('note', testText);
      const note = loadNote();
      expect(note).toBe(testText);
    });

    it('should return empty string if no note exists', () => {
      const note = loadNote();
      expect(note).toBe('');
    });
  });

  describe('Integration', () => {
    it('should save and load note correctly', () => {
      const testText = 'Test integration';
      
      // Save the note
      saveNote(testText);
      
      // Load the note
      const loadedNote = loadNote();
      
      // Verify
      expect(loadedNote).toBe(testText);
    });
  });
});

// Helper function to run tests
function runTests() {
  const testResults = {
    total: 0,
    passed: 0,
    failed: 0,
    errors: []
  };

  function runTest(name, testFn) {
    testResults.total++;
    try {
      testFn();
      testResults.passed++;
      console.log(`✅ ${name}`);
    } catch (error) {
      testResults.failed++;
      testResults.errors.push({ name, error });
      console.error(`❌ ${name}\n   ${error.message}`);
    }
  }


  // Run tests
  console.log('\nRunning Tests...\n');
  
  // Run all test suites
  Object.values(global.describe.tests).forEach(suite => {
    console.log(`\n${suite.name}`);
    suite.tests.forEach(test => {
      runTest(test.name, test.fn);
    });
  });

  // Print summary
  console.log('\nTest Summary:');
  console.log(`Total: ${testResults.total}`);
  console.log(`Passed: ${testResults.passed}`);
  console.log(`Failed: ${testResults.failed}`);
  
  if (testResults.failed > 0) {
    console.log('\nFailed Tests:');
    testResults.errors.forEach(({ name, error }) => {
      console.log(`\n${name}:`);
      console.log(`  ${error.message}`);
    });
    process.exit(1);
  }
  
  process.exit(0);
}

// Run tests if this file is executed directly
if (require.main === module) {
  runTests();
}