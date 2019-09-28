import * as child_process from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import * as log from './log';
import {loadProject} from './ProjectFile';

export class Library {
	libpath: string;
	libroot: string;
}

export class Target {
	baseTarget: string;
	backends: string[];

	constructor(baseTarget: string, backends: string[]) {
		this.baseTarget = baseTarget;
		this.backends = backends;
	}
}

function contains(main: string, sub: string) {
	main = path.resolve(main);
	sub = path.resolve(sub);
	if (process.platform === 'win32') {
		main = main.toLowerCase();
		sub = sub.toLowerCase();
	}
	return sub.indexOf(main) === 0 && sub.slice(main.length)[0] === path.sep;
}

export class Project {
	static platform: string;
	static scriptdir: string;
	name: string;
	version: string;
	sources: string[];
	defines: string[];
	cdefines: string[];
	parameters: string[];
	scriptdir: string;
	libraries: Library[];
	localLibraryPath: string;
	windowOptions: any;
	targetOptions: any;
	assetMatchers: { match: string, options: any }[];
	shaderMatchers: { match: string, options: any }[];
	customTargets: Map<string, Target>;
	stackSize: number;
	id: string;
	icon: string = null;

	constructor(name: string) {
		this.name = name;
		this.version = '1.0';
		this.sources = [];
		this.defines = ['hxcpp_smart_strings'];
		this.cdefines = [];
		this.parameters = [];
		this.scriptdir = Project.scriptdir;
		this.libraries = [];
		this.localLibraryPath = 'Libraries';
		this.assetMatchers = [];
		this.shaderMatchers = [];
		this.customTargets = new Map();
		this.stackSize = 0;

		this.windowOptions = {};
		this.targetOptions = {
			html5: {},
			flash: {},
			android: {},
			android_native: {},
			ios: {},
			xboxOne: {},
			playStation4: {},
			switch: {}
		};
	}

	async addProject(projectDir: string) {
		let project = await loadProject(projectDir, 'khafile.js', Project.platform);
		this.assetMatchers = this.assetMatchers.concat(project.assetMatchers);
		this.sources = this.sources.concat(project.sources);
		this.shaderMatchers = this.shaderMatchers.concat(project.shaderMatchers);
		this.defines = this.defines.concat(project.defines);
		this.cdefines = this.cdefines.concat(project.cdefines);
		this.parameters = this.parameters.concat(project.parameters);
		this.libraries = this.libraries.concat(project.libraries);
		for (let customTarget of project.customTargets.keys()) {
			this.customTargets.set(customTarget, project.customTargets.get(customTarget));
		}
		// windowOptions and targetOptions are ignored
	}

	private unglob(str: string): string {
		const globChars = ['\\@', '\\!', '\\+', '\\*', '\\?', '\\(', '\\[', '\\{', '\\)', '\\]', '\\}'];
		str = str.replace(/\\/g, '/');
		for (const char of globChars) {
			str = str.replace(new RegExp(char, 'g'), '\\' + char.substr(1));
		}
		return str;
	}

	/**
	 * Add all assets matching the match glob relative to the directory containing the current khafile.
	 * Asset types are infered from the file suffix.
	 * Glob syntax is very simple, the most important patterns are * for anything and ** for anything across directories.
	 */
	addAssets(match: string, options: any) {
		if (!options) options = {};

		if (!path.isAbsolute(match)) {
			let base = this.unglob(path.resolve(this.scriptdir));
			if (!base.endsWith('/')) {
				base += '/';
			}
			match = base + match.replace(/\\/g, '/');
		}

		this.assetMatchers.push({ match: match, options: options });
	}

	addSources(source: string) {
		this.sources.push(path.resolve(path.join(this.scriptdir, source)));
	}

	/**
	 * Add all shaders matching the match glob relative to the directory containing the current khafile.
	 * Glob syntax is very simple, the most important patterns are * for anything and ** for anything across directories.
	 */
	addShaders(match: string, options: any) {
		if (!options) options = {};

		if (!path.isAbsolute(match)) {
			let base = this.unglob(path.resolve(this.scriptdir));
			if (!base.endsWith('/')) {
				base += '/';
			}
			match = base + match.replace(/\\/g, '/');
		}

		this.shaderMatchers.push({ match: match, options: options });
	}

	addDefine(define: string) {
		this.defines.push(define);
	}

	addCDefine(define: string) {
		this.cdefines.push(define);
	}

	addParameter(parameter: string) {
		this.parameters.push(parameter);
	}

	addTarget(name: string, baseTarget: string, backends: string[]) {
		this.customTargets.set(name, new Target(baseTarget, backends));
	}

	addLibrary(library: string) {
		this.addDefine(library);
		let self = this;
		function findLibraryDirectory(name: string) {
			if (path.isAbsolute(name)) {
				return { libpath: name, libroot: name };
			}

			// check relative path
			if (fs.existsSync(path.resolve(name))) {
				return { libpath: name, libroot: name };
			}

			// Tries to load the default library from inside the kha project.
			// e.g. 'Libraries/wyngine'
			let libpath = path.join(self.scriptdir, self.localLibraryPath, name);
			if (fs.existsSync(libpath) && fs.statSync(libpath).isDirectory()) {
				return { libpath: path.resolve(libpath), libroot: self.localLibraryPath + '/' + name };
			}
			// If the library couldn't be found in Libraries folder, try
			// looking in the haxelib folders.
			// e.g. addLibrary('hxcpp') => '/usr/lib/haxelib/hxcpp/3,2,193'
			try {
				libpath = path.join(child_process.execSync('haxelib config', { encoding: 'utf8' }).trim(), name.replace(/\./g, ','));
			}
			catch (error) {
				if (process.env.HAXEPATH) {
					libpath = path.join(process.env.HAXEPATH, 'lib', name.toLowerCase());
				}
			}
			if (fs.existsSync(libpath) && fs.statSync(libpath).isDirectory()) {
				if (fs.existsSync(path.join(libpath, '.dev'))) {
					return { libpath: fs.readFileSync(path.join(libpath, '.dev'), 'utf8'), libroot: libpath };
				}
				else if (fs.existsSync(path.join(libpath, '.current'))) {
					// Get the latest version of the haxelib path,
					// e.g. for 'hxcpp', latest version '3,2,193'
					let current = fs.readFileSync(path.join(libpath, '.current'), 'utf8');
					return { libpath: path.join(libpath, current.replace(/\./g, ',')), libroot: libpath };
				}
			}
			// Show error if library isn't found in Libraries or haxelib folder
			log.error('Error: Library ' + name + ' not found.');
			log.error('Add it to the \'Libraries\' subdirectory of your project. You may also install it via haxelib but that\'s less cool.');
			throw 'Library ' + name + ' not found.';
		}

		let libInfo = findLibraryDirectory(library);
		let dir = libInfo.libpath;

		if (dir !== '') {
			this.libraries.push({
				libpath: dir,
				libroot: libInfo.libroot
			});
			// If this is a haxelib library, there must be a haxelib.json
			if (fs.existsSync(path.join(dir, 'haxelib.json'))) {
				let options = JSON.parse(fs.readFileSync(path.join(dir, 'haxelib.json'), 'utf8'));
				// If there is a classPath value, add that directory to be loaded.
				// Otherwise, just load the current path.
				if (options.classPath) {
					// TODO find an example haxelib that has a classPath value
					this.sources.push(path.join(dir, options.classPath));
				}
				else {
					// e.g. '/usr/lib/haxelib/hxcpp/3,2,193'
					this.sources.push(dir);
				}
				// If this haxelib has other library dependencies, add them too
				if (options.dependencies) {
					for (let dependency in options.dependencies) {
						if (dependency.toLowerCase() !== 'kha') {
							this.addLibrary(dependency);
						}
					}
				}
			}
			else {
				// If there is no haxelib.json file, then just load the library
				// by the Sources folder.
				// e.g. Libraries/wyngine/Sources
				if (!fs.existsSync(path.join(dir, 'Sources'))) {
					log.info('Warning: No haxelib.json and no Sources directory found in library ' + library + '.');
				}
				this.sources.push(path.join(dir, 'Sources'));
			}

			if (fs.existsSync(path.join(dir, 'extraParams.hxml'))) {
				let params = fs.readFileSync(path.join(dir, 'extraParams.hxml'), 'utf8');
				for (let parameter of params.split('\n')) {
					let param = parameter.trim();
					if (param !== '') {
						if (param.startsWith('-lib')) {
							// (DK)
							//  - '-lib xxx' is for linking a library via haxe, it forces the use of the haxelib version
							//  - this should be handled by khamake though, as it tracks the dependencies better (local folder or haxelib)
							log.info('Ignoring ' + dir + '/extraParams.hxml "' + param + '"');
						}
						else {
							this.addParameter(param);
						}
					}
				}
			}

			this.addShaders(dir + '/Sources/Shaders/**', {});
		}
	}
}
