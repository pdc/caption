/* Style-sheet switcher

Ideas stolen from http://alistapart.com/stories/alternate/

This script defines functions and then sets the current
style sheet based on a cookie, or failing that, using the
preferred style sheet. For this to work, the 'script' element
that links to this script MUST come after any 'link' elements.

*/

// Given the title of a style sheet, make that the one that is active.
function setActiveStyleSheet(desiredTitle) {
	var elts = document.getElementsByTagName('link');
	for (var i = 0; i < elts.length; ++i) {
		var elt = elts[i];
		if (elt.getAttribute('rel').indexOf('style') >= 0 
				&& elt.getAttribute('title')) {
			// This is a switchable style-sheet link.
			elt.disabled = (elt.getAttribute('title') != desiredTitle);
		}
	}
}

// Return the title of the active style sheet.
function getActiveStyleSheet() {
	var elts = document.getElementsByTagName('link');
	for (var i = 0; i < elts.length; ++i) {
		var elt = elts[i];
		if (elt.getAttribute('rel').indexOf('style') >= 0 
				&& elt.getAttribute('title')
				&& !elt.disabled) {
			return elt.getAttribute('title');
		}
	}	
	return null;
}

// Return the style sheet that is activated by default.
function getPreferredStyleSheet() {
	var elts = document.getElementsByTagName('link');
	for (var i = 0; i < elts.length; ++i) {
		var elt = elts[i];
		if (elt.getAttribute('rel').indexOf('style') >= 0 
				&& elt.getAttribute('title')
				&& elt.getAttribute('rel').indexOf('alt') < 0) {
			return elt.getAttribute('title');
		}
	}	
	return null;
}

var styleSheetMenuItems = {};

function createStyleMenu(id) {
	var ulElt = document.getElementById(id);
	while (ulElt.childNodes.length > 0) {
		ulElt.removeChild(ulElt.firstChild);
	}
	var elts = document.getElementsByTagName('link');
	for (var i = 0; i < elts.length; ++i) {
		var elt = elts[i];
		if (elt.getAttribute('rel').indexOf('style') >= 0
				&& elt.getAttribute('title')) {
			var title = elt.getAttribute('title');
			if (!styleSheetMenuItems[title]) {
				var liElt = document.createElement('li');
				ulElt.appendChild(liElt);
				
				var aElt = document.createElement('a');
				liElt.appendChild(aElt);
				aElt.href = '#';
				aElt.onclick = function () {
					onStyleSheetMenuItemClick(this.styleSheet);
				}
				aElt.styleSheet = title;
				aElt.appendChild(document.createTextNode(title));
				styleSheetMenuItems[title] = aElt;
			}				
		}
	}
	styleSheetMenuItems[getActiveStyleSheet()].className = 'activeStyleSheet';
}

function onStyleSheetMenuItemClick(title) {
	setActiveStyleSheet(title);
	for (var i in styleSheetMenuItems) {
		var elt = styleSheetMenuItems[i];
		elt.className = (i == title ? 'activeStyleSheet' : '');
	}
}


// Add a cookie with this name and value.
// If the days parameter is supplied, make
// a cookie that lasts that many days.
// Otherwise create a session cookie that
// expires when the user's web browser is closed.
function writeCookie(cookieName, value, days) {
	var cookieDef = cookieName + '=' + escape(value) + '; path=/';
	if (days > 0) {
		var date = new Date();
		date.setTime(date.getTime() + days*24*60*60*1000);
		cookieDef += "; expires="+date.toGMTString();
	}
	document.cookie = cookieDef;
}

// Look for a cookie with this name.
// If there is one, return its value.
// Otherwise return null.
function readCookie(cookieName) {
	var cookieDefs = document.cookie.split(';');
	for (var i = 0; i < cookieDefs.length; ++i) {
		var cookieDef = cookieDefs[i];
		while (cookieDef.charAt(0)==' ') {
			cookieDef = cookieDef.substring(1);
		}
		var parts = cookieDef.split('=', 2);
		if (parts[0] == cookieName) {
			return unescape(parts[1]);
		}
	}
	return null;
}

// This sets the style to match the preferred style.
var title = readCookie('style');
if (!title) {
	title = getPreferredStyleSheet();
}
setActiveStyleSheet(title);

// Arrange to create the style menu.
window.onload = function () {
	createStyleMenu('style_menu');
}

// Arrange to take note of the style when the window closes.
window.onunload = function () {
	var title = getActiveStyleSheet();
	writeCookie('style', title);
}

