#include "pch.h"

#include <Kore/Input/Gamepad.h>
#include <Kore/Input/HIDManager.h>
#include <Kore/Log.h>

using namespace Kore;

HIDManager::HIDManager() : managerRef(0x0) {
	initHIDManager();
}

HIDManager::~HIDManager() {
	if (managerRef) {
		IOHIDManagerUnscheduleFromRunLoop(managerRef, CFRunLoopGetCurrent(), kCFRunLoopDefaultMode);
		IOHIDManagerClose(managerRef, kIOHIDOptionsTypeNone);
	}
}

int HIDManager::initHIDManager() {
	// Initialize the IOHIDManager
	managerRef = IOHIDManagerCreate(kCFAllocatorDefault, kIOHIDOptionsTypeNone);
	if (CFGetTypeID(managerRef) == IOHIDManagerGetTypeID()) {

		// Create a matching dictionary for gamepads and joysticks
		CFMutableArrayRef matchingCFArrayRef = CFArrayCreateMutable(kCFAllocatorDefault, 0, &kCFTypeArrayCallBacks);
		if (matchingCFArrayRef) {
			// Create a device matching dictionary for joysticks
			CFDictionaryRef matchingCFDictRef = createDeviceMatchingDictionary(kHIDPage_GenericDesktop, kHIDUsage_GD_Joystick);
			addMatchingArray(matchingCFArrayRef, matchingCFDictRef);

			// Create a device matching dictionary for game pads
			matchingCFDictRef = createDeviceMatchingDictionary(kHIDPage_GenericDesktop, kHIDUsage_GD_GamePad);
			addMatchingArray(matchingCFArrayRef, matchingCFDictRef);
		}
		else {
			Kore::log(Error, "%s: CFArrayCreateMutable failed.", __PRETTY_FUNCTION__);
			return -1;
		}

		// Set the HID device matching array
		IOHIDManagerSetDeviceMatchingMultiple(managerRef, matchingCFArrayRef);
		CFRelease(matchingCFArrayRef);

		// Open manager
		IOHIDManagerOpen(managerRef, kIOHIDOptionsTypeNone);

		// Register routines to be called when (matching) devices are connected or disconnected
		IOHIDManagerRegisterDeviceMatchingCallback(managerRef, deviceConnected, this);
		IOHIDManagerRegisterDeviceRemovalCallback(managerRef, deviceRemoved, this);

		IOHIDManagerScheduleWithRunLoop(managerRef, CFRunLoopGetCurrent(), kCFRunLoopDefaultMode);

		return 0;
	}
	return -1;
}

bool HIDManager::addMatchingArray(CFMutableArrayRef matchingCFArrayRef, CFDictionaryRef matchingCFDictRef) {
	if (matchingCFDictRef) {
		// Add it to the matching array
		CFArrayAppendValue(matchingCFArrayRef, matchingCFDictRef);
		CFRelease(matchingCFDictRef); // and release it
		return true;
	}
	return false;
}

CFMutableDictionaryRef HIDManager::createDeviceMatchingDictionary(u32 inUsagePage, u32 inUsage) {
	// Create a dictionary to add usage page/usages to
	CFMutableDictionaryRef result = CFDictionaryCreateMutable(kCFAllocatorDefault, 0, &kCFTypeDictionaryKeyCallBacks, &kCFTypeDictionaryValueCallBacks);
	if (result) {
		if (inUsagePage) {
			// Add key for device type to refine the matching dictionary.
			CFNumberRef pageCFNumberRef = CFNumberCreate(kCFAllocatorDefault, kCFNumberIntType, &inUsagePage);
			if (pageCFNumberRef) {
				CFDictionarySetValue(result, CFSTR(kIOHIDDeviceUsagePageKey), pageCFNumberRef);
				CFRelease(pageCFNumberRef);

				// note: the usage is only valid if the usage page is also defined
				if (inUsage) {
					CFNumberRef usageCFNumberRef = CFNumberCreate(kCFAllocatorDefault, kCFNumberIntType, &inUsage);
					if (usageCFNumberRef) {
						CFDictionarySetValue(result, CFSTR(kIOHIDDeviceUsageKey), usageCFNumberRef);
						CFRelease(usageCFNumberRef);
					}
					else {
						log(Error, "%s: CFNumberCreate(usage) failed.", __PRETTY_FUNCTION__);
					}
				}
			}
			else {
				log(Error, "%s: CFNumberCreate(usage page) failed.", __PRETTY_FUNCTION__);
			}
		}
	}
	else {
		log(Error, "%s: CFDictionaryCreateMutable failed.", __PRETTY_FUNCTION__);
	}
	return result;
}

// HID device plugged callback
void HIDManager::deviceConnected(void* inContext, IOReturn inResult, void* inSender, IOHIDDeviceRef inIOHIDDeviceRef) {
	// Reference manager
	HIDManager *manager = (HIDManager*) inContext;

	// Find an empty slot in the devices list and add the new device there
	// TODO: does this need to be made thread safe?
	DeviceRecord *device = manager->devices;
	for (int i = 0; i < MAX_DEVICES; ++i, ++device) {
		if (!device->connected) {
			device->connected	= true;
			device->device 		= inIOHIDDeviceRef;
			device->pad.bind(inIOHIDDeviceRef, i);
			break;
		}
	}
}

// HID device unplugged callback
void HIDManager::deviceRemoved(void* inContext, IOReturn inResult, void* inSender, IOHIDDeviceRef inIOHIDDeviceRef) {
	// Reference manager
	HIDManager *manager = (HIDManager*) inContext;

	// TODO: does this need to be made thread safe?
	DeviceRecord *device = manager->devices;
	for (int i = 0; i < MAX_DEVICES; ++i, ++device) {
		// TODO: is comparing IOHIDDeviceRef to match devices safe? Is there a better way?
		if (device->connected && device->device == inIOHIDDeviceRef) {
			device->connected	= false;
			device->device 		= nullptr;
			device->pad.unbind();
			break;
		}
	}
}
