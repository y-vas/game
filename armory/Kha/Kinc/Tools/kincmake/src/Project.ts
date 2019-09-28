import * as fs from 'fs-extra';
import * as path from 'path';
import * as log from './log';
import {GraphicsApi} from './GraphicsApi';
import {Architecture} from './Architecture';
import {AudioApi} from './AudioApi';
import {VrApi} from './VrApi';
import {RayTraceApi} from './RayTraceApi';
import {Options} from './Options';
import {Platform} from './Platform';
const uuid = require('uuid');

function getDefines(platform: string, rotated: boolean) {
	let defines: string[] = [];
	switch (platform) {
		case Platform.iOS:
			if (rotated) defines.push('ROTATE90');
			break;
		case Platform.Android:
			if (rotated) defines.push('ROTATE90');
			break;
	}
	return defines;
}

function contains(array: any[], value: any) {
	for (const element of array) {
		if (element === value) return true;
	}
	return false;
}

function containsDefine(array: Define[], value: Define) {
	for (const element of array) {
		if (element.value === value.value && element.config === value.config) return true;
	}
	return false;
}

function isAbsolute(path: string) {
	return (path.length > 0 && path[0] === '/') || (path.length > 1 && path[1] === ':');
}

let projectInProgress = 0;

process.on('exit', (code: number) => {
	if (projectInProgress > 0) {
		console.error('Error: korefile did not call resolve, no project created.');
	}
});

let scriptdir = '.';
// let lastScriptDir = '.';
let koreDir = '.';

async function loadProject(directory: string, korefile: string = 'kincfile.js'): Promise<Project> {
	return new Promise<Project>((resolve, reject) => {
		projectInProgress += 1;
		let resolver = async (project: Project) => {
			projectInProgress -= 1;

			// TODO: This accidentally finds Kha/Backends/KoreHL
			/*if (fs.existsSync(path.join(scriptdir, 'Backends'))) {
				var libdirs = fs.readdirSync(path.join(scriptdir, 'Backends'));
				for (var ld in libdirs) {
					var libdir = path.join(scriptdir, 'Backends', libdirs[ld]);
					if (fs.statSync(libdir).isDirectory()) {
						var korefile = path.join(libdir, korefile);
						if (fs.existsSync(korefile)) {
							project.addSubProject(await Project.createProject(libdir, scriptdir));
						}
					}
				}
			}*/

			resolve(project);
		};

		try {
			scriptdir = directory;
			let file = fs.readFileSync(path.resolve(directory, korefile), 'utf8');
			let AsyncFunction = Object.getPrototypeOf(async () => {}).constructor;
			let project = new AsyncFunction(
				'log',
				'Project',
				'Platform',
				'platform',
				'GraphicsApi',
				'graphics',
				'Architecture',
				'arch',
				'AudioApi',
				'audio',
				'VrApi',
				'vr',
				'RayTraceApi',
				'raytrace',
				'require',
				'resolve',
				'reject',
				'__dirname',
				file)
			(
				log,
				Project,
				Platform,
				Project.platform,
				GraphicsApi,
				Options.graphicsApi,
				Architecture,
				Options.architecture,
				AudioApi,
				Options.audioApi,
				VrApi,
				Options.vrApi,
				RayTraceApi,
				Options.rayTraceApi,
				require,
				resolver,
				reject,
				directory);
			}
		catch (error) {
			log.error(error);
			throw error;
		}
	});
}

export interface File {
	file: string;
	options: any;
	projectDir: string;
	projectName: string;
}

export class Define {
	value: string;
	config: string;
}

export class Project {
	static platform: string;
	static koreDir: string;
	static root: string;
	name: string;
	version: string;
	id: string;
	debugDir: string;
	basedir: string;
	uuid: string;
	files: File[];
	javadirs: string[];
	subProjects: Project[];
	includeDirs: string[];
	defines: Define[];
	libs: string[];
	systemDependendLibraries: any;
	includes: {file: string, options: any}[];
	excludes: string[];
	customs: {file: string, command: string, output: string}[];
	cpp11: boolean;
	c11: boolean;
	kore: boolean;
	targetOptions: any;
	rotated: boolean;
	cmd: boolean;
	cFlags: string[] = [];
	cppFlags: string[] = [];
	stackSize: number;
	icon: string = null;

	constructor(name: string) {
		this.name = name;
		this.version = '1.0';
		this.debugDir = '';
		this.basedir = scriptdir;
		this.uuid = uuid.v4();

		this.files = [];
		this.customs = [];
		this.javadirs = [];
		this.subProjects = [];
		this.includeDirs = [];
		this.defines = [];
		this.libs = [];
		this.systemDependendLibraries = {};
		this.includes = [];
		this.excludes = [];
		this.cpp11 = false;
		this.c11 = false;
		this.kore = true;
		this.targetOptions = {
			android: {},
			xboxOne: {},
			playStation4: {},
			switch: {}
		};
		this.rotated = false;
		this.cmd = false;
		this.stackSize = 0;
	}

	flatten() {
		for (let sub of this.subProjects) sub.flatten();
		for (let sub of this.subProjects) {
			if (sub.cpp11) {
				this.cpp11 = true;
			}
			if (sub.c11) {
				this.c11 = true;
			}
			if (sub.cmd) {
				this.cmd = true;
			}
			let subbasedir = sub.basedir;

			for (let tkey of Object.keys(sub.targetOptions)) {
				const target = sub.targetOptions[tkey];
				for (let key of Object.keys(target)) {
					const options = this.targetOptions[tkey];
					const option = target[key];
					if (options[key] == null) options[key] = option;
					// push library properties to current array instead
					else if (Array.isArray(options[key]) && Array.isArray(option)) {
						for (let value of option) {
							if (!options[key].includes(value)) options[key].push(value);
						}
					}
				}
			}

			for (let d of sub.defines) if (!containsDefine(this.defines, d)) this.defines.push(d);
			for (let file of sub.files) {
				let absolute = file.file;
				if (!path.isAbsolute(absolute)) {
					absolute = path.join(subbasedir, file.file);
				}
				this.files.push({file: absolute.replace(/\\/g, '/'), options: file.options, projectDir: subbasedir, projectName: sub.name });
			}
			for (const custom of sub.customs) {
				let absolute = custom.file;
				if (!path.isAbsolute(absolute)) {
					absolute = path.join(subbasedir, custom.file);
				}
				this.customs.push({file: absolute.replace(/\\/g, '/'), command: custom.command, output: custom.output });
			}
			for (let i of sub.includeDirs) if (!contains(this.includeDirs, path.resolve(subbasedir, i))) this.includeDirs.push(path.resolve(subbasedir, i));
			for (let j of sub.javadirs) if (!contains(this.javadirs, path.resolve(subbasedir, j))) this.javadirs.push(path.resolve(subbasedir, j));
			for (let lib of sub.libs) {
				if (lib.indexOf('/') < 0 && lib.indexOf('\\') < 0) {
					if (!contains(this.libs, lib)) this.libs.push(lib);
				}
				else {
					if (!contains(this.libs, path.resolve(subbasedir, lib))) this.libs.push(path.resolve(subbasedir, lib));
				}
			}
			for (let system in sub.systemDependendLibraries) {
				let libs = sub.systemDependendLibraries[system];
				for (let lib of libs) {
					if (this.systemDependendLibraries[system] === undefined) this.systemDependendLibraries[system] = [];
					if (!contains(this.systemDependendLibraries[system], this.stringify(path.resolve(subbasedir, lib)))) {
						if (!contains(lib, '/') && !contains(lib, '\\')) this.systemDependendLibraries[system].push(lib);
						else this.systemDependendLibraries[system].push(this.stringify(path.resolve(subbasedir, lib)));
					}
				}
			}
			for (let flag of sub.cFlags) {
				if (!this.cFlags.includes(flag)) {
					this.cFlags.push(flag);
				}
			}
			for (let flag of sub.cppFlags) {
				if (!this.cppFlags.includes(flag)) {
					this.cppFlags.push(flag);
				}
			}
		}
		this.subProjects = [];
	}

	getName() {
		return this.name;
	}

	getUuid() {
		return this.uuid;
	}

	matches(text: string, pattern: string) {
		const regexstring = pattern.replace(/\./g, '\\.').replace(/\*\*/g, '.?').replace(/\*/g, '[^/]*').replace(/\?/g, '*');
		const regex = new RegExp('^' + regexstring + '$', 'g');
		return regex.test(text);
	}

	matchesAllSubdirs(dir: string, pattern: string) {
		if (pattern.endsWith('/**')) {
			return this.matches(this.stringify(dir), pattern.substr(0, pattern.length - 3));
		}
		else return false;
	}

	stringify(path: string) {
		return path.replace(/\\/g, '/');
	}

	addCFlag(flag: string) {
		this.cFlags.push(flag);
	}

	addCFlags() {
		for (let i = 0; i < arguments.length; ++i) {
			if (typeof arguments[i] === 'string') {
				this.addCFlag(arguments[i]);
			}
		}
	}

	addCppFlag(flag: string) {
		this.cppFlags.push(flag);
	}

	addCppFlags() {
		for (let i = 0; i < arguments.length; ++i) {
			if (typeof arguments[i] === 'string') {
				this.addCppFlag(arguments[i]);
			}
		}
	}

	addFileForReal(file: string, options: any) {
		for (let index in this.files) {
			if (this.files[index].file === file) {
				this.files[index] = {file: file, options: options, projectDir: this.basedir, projectName: this.name};
				return;
			}
		}
		this.files.push({file: file, options: options, projectDir: this.basedir, projectName: this.name});
	}

	searchFiles(current: any) {
		if (current === undefined) {
			for (let sub of this.subProjects) sub.searchFiles(undefined);
			this.searchFiles(this.basedir);
			for (let includeobject of this.includes) {
				if (includeobject.file.startsWith('../')) {
					let start = '../';
					while (includeobject.file.startsWith(start)) {
						start += '../';
					}
					this.searchFiles(path.resolve(this.basedir, start));
				}
			}
			// std::set<std::string> starts;
			// for (std::string include : includes) {
			//     if (!isAbsolute(include)) continue;
			//     std::string start = include.substr(0, firstIndexOf(include, '*'));
			//     if (starts.count(start) > 0) continue;
			//     starts.insert(start);
			//     searchFiles(Paths::get(start));
			// }
			return;
		}

		let files = fs.readdirSync(current);
		nextfile: for (let f in files) {
			let file = path.join(current, files[f]);
			if (fs.statSync(file).isDirectory()) continue;
			// if (!current.isAbsolute())
			file = path.relative(this.basedir, file);
			for (let exclude of this.excludes) {
				if (this.matches(this.stringify(file), exclude)) continue nextfile;
			}
			for (let includeobject of this.includes) {
				let include = includeobject.file;
				if (isAbsolute(include)) {
					let inc = include;
					inc = path.relative(this.basedir, inc);
					include = inc;
				}
				if (this.matches(this.stringify(file), include)) {
					this.addFileForReal(this.stringify(file), includeobject.options);
				}
			}
		}

		let dirs = fs.readdirSync(current);
		nextdir: for (let d of dirs) {
			let dir = path.join(current, d);
			if (d.startsWith('.')) continue;
			if (!fs.statSync(dir).isDirectory()) continue;
			for (let exclude of this.excludes) {
				if (this.matchesAllSubdirs(path.relative(this.basedir, dir), exclude)) {
					continue nextdir;
				}
			}
			this.searchFiles(dir);
		}
	}

	addFile(file: string, options: any) {
		this.includes.push({file: file, options: options});
	}

	addCustomFile(file: string, command: string, output: string) {
		this.customs.push({file, command, output});
	}

	addFiles() {
		let options: any = undefined;
		for (let i = 0; i < arguments.length; ++i) {
			if (typeof arguments[i] !== 'string') {
				options = arguments[i];
			}
		}
		for (let i = 0; i < arguments.length; ++i) {
			if (typeof arguments[i] === 'string') {
				this.addFile(arguments[i], options);
			}
		}
	}

	addJavaDir(dir: string) {
		this.javadirs.push(dir);
	}

	addJavaDirs() {
		for (let i = 0; i < arguments.length; ++i) {
			this.addJavaDir(arguments[i]);
		}
	}

	addExclude(exclude: string) {
		this.excludes.push(exclude);
	}

	addExcludes() {
		for (let i = 0; i < arguments.length; ++i) {
			this.addExclude(arguments[i]);
		}
	}

	addDefine(value: string, config: string = null) {
		const define = {value, config};
		if (containsDefine(this.defines, define)) return;
		this.defines.push(define);
	}

	addDefines() {
		for (let i = 0; i < arguments.length; ++i) {
			this.addDefine(arguments[i]);
		}
	}

	addIncludeDir(include: string) {
		if (contains(this.includeDirs, include)) return;
		this.includeDirs.push(include);
	}

	addIncludeDirs() {
		for (let i = 0; i < arguments.length; ++i) {
			this.addIncludeDir(arguments[i]);
		}
	}

	addLib(lib: string) {
		this.libs.push(lib);
	}

	addLibs() {
		for (let i = 0; i < arguments.length; ++i) {
			this.addLib(arguments[i]);
		}
	}

	addLibFor(system: string, lib: string) {
		if (this.systemDependendLibraries[system] === undefined) this.systemDependendLibraries[system] = [];
		this.systemDependendLibraries[system].push(lib);
	}

	addLibsFor() {
		if (this.systemDependendLibraries[arguments[0]] === undefined) this.systemDependendLibraries[arguments[0]] = [];
		for (let i = 1; i < arguments.length; ++i) {
			this.systemDependendLibraries[arguments[0]].push(arguments[i]);
		}
	}

	getFiles() {
		return this.files;
	}

	getJavaDirs() {
		return this.javadirs;
	}

	getBasedir() {
		return this.basedir;
	}

	getSubProjects() {
		return this.subProjects;
	}

	getIncludeDirs() {
		return this.includeDirs;
	}

	getDefines() {
		return this.defines;
	}

	getLibs() {
		return this.libs;
	}

	getLibsFor(system: string) {
		if (this.systemDependendLibraries[system] === undefined) return [];
		return this.systemDependendLibraries[system];
	}

	getDebugDir() {
		return this.debugDir;
	}

	setDebugDir(debugDir: string) {
		this.debugDir = path.resolve(this.basedir, debugDir);
	}

	async addProject(directory: string) {
		this.subProjects.push(await loadProject(path.isAbsolute(directory) ? directory : path.join(this.basedir, directory)));
	}

	static async create(directory: string, platform: string, korefile: string) {
		Project.koreDir = path.join(__dirname, '../../..');
		Project.platform = platform;
		let project = await loadProject(path.resolve(directory), korefile);
		if (project.kore) {
			await project.addProject(Project.koreDir);
		}
		let defines = getDefines(platform, project.isRotated());
		for (let define of defines) {
			project.addDefine(define);
		}
		return project;
	}

	isRotated() {
		return this.rotated;
	}

	isCmd() {
		return this.cmd;
	}

	setRotated() {
		this.rotated = true;
	}

	setCmd() {
		this.cmd = true;
	}

	// deprecated
	static createProject(): Promise<void> {
		log.info('Warning: createProject was removed, see updates.md for instructions.');
		return new Promise<void>((resolve, reject) => {
			resolve();
		});
	}

	// deprecated
	addSubProject() {

	}
}
