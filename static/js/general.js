// general.js

$(document).ready(function() {
  $(document).foundation();
  window.onhashchange = hasher;
  hasher();
});

function setData() {
	$.each(config, function(key,value) {
		$(".data-"+key).text(value);
	});
}

function loader(div,url,cb) {
	div.empty();
	div.load(url, function(response, status, xhr) {
		if (cb && typeof cb === "function") cb(xhr);
    setData();
	});
}

String.prototype.capitalize = function() {
	if (this.length <= 1) return this;
	var words = this.split(" ");
	for (var i in words)
		if (words[i][0] && words[i][0].match(/[A-Za-z]/))
			words[i] = words[i].replace(new RegExp(words[i][0]),words[i][0].toUpperCase());
	return words.join(" ");
}
