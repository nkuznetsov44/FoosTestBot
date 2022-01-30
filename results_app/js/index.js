const wrapper = document.getElementById('users-table');

function fetchUsers() {
  fetch('/api/users')
      .then(data => data.json())
      .then(jsonData => populate(jsonData))
      .catch(e => {
          console.log(e);
      });
};

document.addEventListener('DOMContentLoaded', fetchUsers, false);

function dom(tag, text) {
    let r = document.createElement(tag);
    if (text) r.innerText = text;
    return r;
};

function append(parent, child) {
  parent.appendChild(child);
  return parent;
};

function populate(json) {
    console.log(json);
    if (json.length === 0) return;
    let keys = Object.keys(json[0]);
    let table = dom('table');
    //header
    append(table,
      keys.map(k => dom('th', k)).reduce(append, dom('tr'))
    );
    //values
    const makeRow = (acc, row) =>
        append(acc,
            keys.map(k => dom('td', row[k])).reduce(append, dom('tr'))
        );
    json.reduce(makeRow, table);
    console.log(table);
    wrapper.appendChild(table);
};