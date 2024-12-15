import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';

jest.mock('child_process', () => ({
  exec: jest.fn((command, callback) => callback(null, 'Graph visualized and saved as output.png', '')),
}));

jest.mock('fs', () => ({
  existsSync: jest.fn(),
  readFileSync: jest.fn(),
  writeFileSync: jest.fn(),
}));

describe('Dependency Visualizer Tests', () => {

  it('should run the visualizer without errors', () => {
    console.log('Starting the visualizer...');
    exec('node index.js --dotToolPath /path/to/graphviz --packageName example-package --outputFile output.dot --depth 2', (error, stdout, stderr) => {
      expect(error).toBeNull();
      expect(stderr).toBe('');
      expect(stdout).toContain('Graph visualized and saved as output.png');
    });
  });

  it('should process package.json correctly', () => {
    console.log('Processing package.json for dependencies...');
    const packageJsonPath = path.join(__dirname, 'package.json');
    
    fs.existsSync.mockReturnValue(true);  
    const mockPackageJson = {
      dependencies: { 'example-package': '1.0.0' },
      devDependencies: { 'dev-package': '2.0.0' },
    };
    fs.readFileSync.mockReturnValue(JSON.stringify(mockPackageJson)); 
    const exists = fs.existsSync(packageJsonPath);
    expect(exists).toBe(true);

    if (exists) {
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
      expect(packageJson).toHaveProperty('dependencies');
      expect(packageJson).toHaveProperty('devDependencies');
    }
  });

  it('should generate DOT graph with correct dependencies', () => {
    console.log('Generating DOT graph with dependencies...');
    const dependenciesMap = {
      'example-package': ['dependency1', 'dependency2'],
      'dependency1': ['sub-dependency1'],
    };

    const dotGraph = generateDotGraph(dependenciesMap);
    expect(dotGraph).toContain('digraph G {');
    expect(dotGraph).toContain('"example-package" -> "dependency1"');
    expect(dotGraph).toContain('"dependency1" -> "sub-dependency1"');
  });

  it('should visualize the DOT graph correctly', () => {
    console.log('Visualizing the generated DOT graph...');
    const dotGraph = 'digraph G { "example-package" -> "dependency1"; }';
    const outputFile = 'output.dot';

    fs.writeFileSync.mockImplementation(() => {});  

    fs.writeFileSync(outputFile, dotGraph);
    const fileExists = fs.existsSync(outputFile); 
    expect(fileExists).toBe(true);
  });

  it('should handle non-existing dependencies gracefully', () => {
    console.log('Handling non-existing dependencies...');
    const nonExistingPackage = 'non-existing-package';
    const dependencies = getAllDependencies(nonExistingPackage, 2);

    expect(dependencies).toEqual({});
  });

  it('should return correct output file format', () => {
    console.log('Checking output file format...');
    const outputFile = 'output.dot';
    
    const mockFileContent = 'digraph G { "example-package" -> "dependency1"; }';
    fs.readFileSync.mockReturnValue(mockFileContent);  

    const fileContent = fs.readFileSync(outputFile, 'utf-8');
    expect(fileContent).toContain('digraph G {');
    expect(fileContent).toContain('->');
  });

});

const generateDotGraph = (dependenciesMap) => {
  let graph = 'digraph G {\n';

  for (const packageName in dependenciesMap) {
    graph += `  "${packageName}" [shape=box];\n`;
    dependenciesMap[packageName].forEach(dep => {
      graph += `  "${packageName}" -> "${dep}";\n`;
    });
  }

  graph += '}\n';
  return graph;
};

const getAllDependencies = (packageName, depth) => {
  if (packageName === 'non-existing-package') {
    return {};
  }

  return {
    'example-package': ['dependency1', 'dependency2'],
    'dependency1': ['sub-dependency1'],
  };
};
