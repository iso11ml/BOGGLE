import * as ko from "https://cdn.skypack.dev/knockout@3.5.1";

function MyFn(settings = {}) {
	const self = this;

	self.elID = settings.elID ?? "";
	self.elToBind =
		settings.elToBind ??
		(self.elID ? document.querySelector("#" + self.ID) : null);

	self.clickCount = ko.observable(0);

	window.addEventListener("resize", () => {});

	self.init = (function () {
		if (self.elToBind) ko.applyBindings(self, self.elToBind);
		else ko.applyBindings(self);
	})();
}

document.addEventListener("DOMContentLoaded", () => {
	const MyVM = new MyFn();
});
