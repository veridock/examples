/**
 * Unit tests for QR Code Generator PWA.SVG Application
 */

// Mock DOM elements
const mockElements = {
  'qr-input': { value: '' },
  'qr-output': { innerHTML: '' }
};

// Mock document for testing
document = {
  getElementById: jest.fn((id) => mockElements[id] || { addEventListener: jest.fn() }),
  querySelector: jest.fn(),
  execCommand: jest.fn(),
  createElement: jest.fn().mockImplementation((tag) => ({
    appendChild: jest.fn(),
    setAttribute: jest.fn(),
    click: jest.fn(),
    style: {}
  })),
  body: {
    appendChild: jest.fn(),
    removeChild: jest.fn()
  }
};

// Mock window.navigator for clipboard API
const mockClipboard = {
  writeText: jest.fn().mockResolvedValue(undefined)
};

global.navigator = {
  clipboard: mockClipboard,
  userAgent: 'node'
};

// Import the functions to test
const { generateQR, copyToClipboard } = require('./qrgen.pwa.svg');

describe('QR Code Generator', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
    mockElements['qr-input'].value = '';
    mockElements['qr-output'].innerHTML = '';
  });

  describe('generateQR', () => {
    it('should generate QR code for valid input', () => {
      const testText = 'https://example.com';
      mockElements['qr-input'].value = testText;
      
      generateQR();
      
      // Verify QR code was generated
      expect(mockElements['qr-output'].innerHTML).toContain('svg');
      expect(mockElements['qr-output'].innerHTML).toContain('qr-code');
    });

    it('should handle empty input', () => {
      mockElements['qr-input'].value = '';
      
      generateQR();
      
      // Should not generate QR code for empty input
      expect(mockElements['qr-output'].innerHTML).toBe('');
    });
  });

  describe('copyToClipboard', () => {
    it('should copy text to clipboard', async () => {
      const testText = 'Test text to copy';
      
      await copyToClipboard(testText);
      
      // Verify clipboard API was called
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith(testText);
    });
  });

  describe('Integration', () => {
    it('should generate and display QR code', () => {
      const testText = 'Test QR Code';
      mockElements['qr-input'].value = testText;
      
      // Generate QR code
      generateQR();
      
      // Verify output contains SVG
      expect(mockElements['qr-output'].innerHTML).toContain('svg');
      
      // Verify input is cleared after generation
      expect(mockElements['qr-input'].value).toBe('');
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
  console.log('\nRunning QR Code Generator Tests...\n');
  
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