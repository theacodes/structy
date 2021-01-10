import _struct from "./struct.mjs";

class Struct {
  constructor(values) {
    for (const field of this.constructor._fields) {
      if (values[field.name] === undefined) {
        this[field.name] = field.default;
      } else {
        this[field.name] = values[field.name];
      }
    }
  }

  static get _struct() {
    return _struct(this._pack_string);
  }

  pack() {
    let values = this.constructor._fields.map((field) => this[field.name]);
    return new Uint8Array(this.constructor._struct.pack(...values));
  }

  static unpack(buf) {
    if (buf instanceof Uint8Array) {
      buf = buf.buffer;
    }

    let unpacked = this._struct.unpack(buf);
    let result = new this();

    for (const field of this._fields) {
      result[field.name] = unpacked.shift();
    }

    return result;
  }
}

export default Struct;
