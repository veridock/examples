/**
 * Unit tests for Stopwatch PWA.SVG Application
 */

// Mock DOM elements and timer functions
const mockElements = {
  'timer': { textContent: '00:00:00' },
  'laps': { innerHTML: '' }
};

// Mock document for testing
document = {
  getElementById: jest.fn((id) => mockElements[id] || { addEventListener: jest.fn() }),
  querySelector: jest.fn(),
  createElement: jest.fn().mockImplementation((tag) => ({
    textContent: '',
    appendChild: jest.fn(),
    style: {}
  }))
};

// Mock timer functions
let mockNow = 0;
global.performance = {
  now: () => mockNow
};

// Mock requestAnimationFrame
let rafCallbacks = [];
global.requestAnimationFrame = (cb) => {
  rafCallbacks.push(cb);
  return rafCallbacks.length;
};

// Mock cancelAnimationFrame
global.cancelAnimationFrame = () => {
  rafCallbacks = [];
};

// Function to simulate time passing
const advanceTimers = (ms) => {
  mockNow += ms;
  const callbacks = [...rafCallbacks];
  rafCallbacks = [];
  callbacks.forEach(cb => cb(mockNow));
};

// Import the Stopwatch class
const { Stopwatch } = require('./stoper.pwa.svg');

describe('Stopwatch', () => {
  let stopwatch;
  
  beforeEach(() => {
    // Reset mocks and create a new Stopwatch instance before each test
    jest.clearAllMocks();
    mockElements.timer.textContent = '00:00:00';
    mockElements.laps.innerHTML = '';
    mockNow = 0;
    rafCallbacks = [];
    
    stopwatch = new Stopwatch();
  });

  describe('Initialization', () => {
    it('should initialize with 00:00:00', () => {
      expect(mockElements.timer.textContent).toBe('00:00:00');
    });
  });

  describe('start()', () => {
    it('should start the stopwatch', () => {
      stopwatch.start();
      advanceTimers(1000);
      expect(mockElements.timer.textContent).not.toBe('00:00:00');
    });
  });

  describe('stop()', () => {
    it('should stop the stopwatch', () => {
      stopwatch.start();
      advanceTimers(1000);
      stopwatch.stop();
      const timeAfterStop = mockElements.timer.textContent;
      advanceTimers(1000);
      expect(mockElements.timer.textContent).toBe(timeAfterStop);
    });
  });

  describe('reset()', () => {
    it('should reset the stopwatch to 00:00:00', () => {
      stopwatch.start();
      advanceTimers(1500);
      stopwatch.reset();
      expect(mockElements.timer.textContent).toBe('00:00:00');
    });
  });

  describe('lap()', () => {
    it('should record lap times', () => {
      stopwatch.start();
      advanceTimers(1000);
      stopwatch.lap();
      expect(mockElements.laps.innerHTML).toContain('Lap 1');
      
      advanceTimers(2000);
      stopwatch.lap();
      expect(mockElements.laps.innerHTML).toContain('Lap 2');
    });
  });

  describe('Integration', () => {
    it('should handle start, lap, stop, and reset sequence', () => {
      // Start the stopwatch
      stopwatch.start();
      
      // Let it run for 1 second
      advanceTimers(1000);
      
      // Record first lap
      stopwatch.lap();
      expect(mockElements.laps.innerHTML).toContain('Lap 1');
      
      // Let it run for 2 more seconds
      advanceTimers(2000);
      
      // Record second lap
      stopwatch.lap();
      expect(mockElements.laps.innerHTML).toContain('Lap 2');
      
      // Stop the stopwatch
      stopwatch.stop();
      const timeAfterStop = mockElements.timer.textContent;
      
      // Verify time doesn't change when stopped
      advanceTimers(1000);
      expect(mockElements.timer.textContent).toBe(timeAfterStop);
      
      // Reset
      stopwatch.reset();
      expect(mockElements.timer.textContent).toBe('00:00:00');
      expect(mockElements.laps.innerHTML).toBe('');
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
  console.log('\nRunning Stopwatch Tests...\n');
  
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