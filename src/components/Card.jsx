import React from "react";
import "../css/Card.css";
import { postGarden } from "../services/garden";
import { useState } from "react";
import happy from "../assets/happy.png";
import sad from "../assets/sad.png";
import Button from "./Button";
import "../css/Formfield.css";
import { FormGroup, Label, Input } from "reactstrap";
import fine from "../assets/fine.png";
import water from "../assets/water-lww.gif";

const Card = ({
  moist_value,
  moist_default,
  is_auto1,
  is_activate1,
  is_auto2,
  is_activate2,
  buzzer,
  sunroof,
}) => {
  const [moist_valuegarden, setMoist_valuegarden] = useState(moist_value);
  const [moist_defaultgarden, setMoist_defultgarden] = useState(0);
  const [is_auto1garden, setIs_auto1] = useState(is_auto1);
  const [is_activate1garden, setis_activate1] = useState(is_activate1);
  const [is_auto2garden, setIs_auto2] = useState(is_auto2);
  const [is_activate2garden, setis_activate2] = useState(is_activate2);
  const [buzzergarden, setBuzzer] = useState(buzzer);
  const [sunroofgarden, setSunroof] = useState(sunroof);

  const handleSubmit = async () => {
    const result = {
      moist_value: moist_value,
      moist_default: moist_defaultgarden,
      sprinkle_1: {
        is_auto: is_auto1,
        is_activate: is_activate1,
      },
      sprinkle_2: {
        is_auto: is_auto2,
        is_activate: is_activate2,
      },
      buzzer: buzzer,
      sunroof: sunroof,
    };
    const res = await postGarden(result);
    console.log(res);
  };
  const handleBuzzer = async () => {
    const result = {
      moist_value: moist_value,
      moist_default: moist_defaultgarden,
      sprinkle_1: {
        is_auto: is_auto1,
        is_activate: is_activate1,
      },
      sprinkle_2: {
        is_auto: is_auto2,
        is_activate: is_activate2,
      },
      buzzer: !buzzer,
      sunroof: sunroof,
    };
    const res = await postGarden(result);
    console.log(res);
  };

  const handleSunroof = async () => {
    const result = {
      moist_value: moist_value,
      moist_default: moist_defaultgarden,
      sprinkle_1: {
        is_auto: is_auto1,
        is_activate: is_activate1,
      },
      sprinkle_2: {
        is_auto: is_auto2,
        is_activate: is_activate2,
      },
      buzzer: buzzer,
      sunroof: !sunroof,
    };
    const res = await postGarden(result);
    console.log(res);
  };

  const handleIs_auto1 = async () => {
    const result = {
      moist_value: moist_value,
      moist_default: moist_defaultgarden,
      sprinkle_1: {
        is_auto: !is_auto1,
        is_activate: is_activate1,
      },
      sprinkle_2: {
        is_auto: is_auto2,
        is_activate: is_activate2,
      },
      buzzer: buzzer,
      sunroof: sunroof,
    };
    const res = await postGarden(result);
    console.log(res);
  };

  const handleIs_activate1 = async () => {
    const result = {
      moist_value: moist_value,
      moist_default: moist_defaultgarden,
      sprinkle_1: {
        is_auto: is_auto1,
        is_activate: !is_activate1,
      },
      sprinkle_2: {
        is_auto: is_auto2,
        is_activate: is_activate2,
      },
      buzzer: buzzer,
      sunroof: sunroof,
    };
    const res = await postGarden(result);
    console.log(res);
  };

  const handleIs_auto2 = async () => {
    const result = {
      moist_value: moist_value,
      moist_default: moist_defaultgarden,
      sprinkle_1: {
        is_auto: is_auto1,
        is_activate: is_activate1,
      },
      sprinkle_2: {
        is_auto: !is_auto2,
        is_activate: is_activate2,
      },
      buzzer: buzzer,
      sunroof: sunroof,
    };
    const res = await postGarden(result);
    console.log(res);
  };

  const handleIs_activate2 = async () => {
    const result = {
      moist_value: moist_value,
      moist_default: moist_defaultgarden,
      sprinkle_1: {
        is_auto: is_auto1,
        is_activate: is_activate1,
      },
      sprinkle_2: {
        is_auto: is_auto2,
        is_activate: !is_activate2,
      },
      buzzer: buzzer,
      sunroof: sunroof,
    };
    const res = await postGarden(result);
    console.log(res);
  };

  const check_photo = (moist_value) => {
    let routeimg = happy;
    if (moist_value < 60) {
      routeimg = sad;
    }
    return routeimg;
  };

  return (
    <div>
      <div className="percent">
        <div className="moistcard">
          <div className="card-head">Moisture</div>
          <div className="percentvalue">{moist_value}%</div>
        </div>
        <div className="status-card">
          <div className="card-head">
            Status
            <span>
              {sunroof === true &&
              buzzer === false &&
              (is_activate2 === true ||
                is_activate1 === true ||
                is_auto1 === true ||
                is_auto2 === true) ? (
                <img src={water} />
              ) : (
                <h4></h4>
              )}
            </span>
          </div>
          <div className="smileimg">
            <img src={check_photo(moist_value)} />
          </div>
          <div
            className={`status-text ${
              moist_value < { moist_default } ? "sad" : "happy"
            }`}
          >
            {moist_value < { moist_default } ? "I need water!!!" : "I'm fine!"}
          </div>
        </div>
      </div>

      <form
        className="form"
        onSubmit={(event) => {
          handleSubmit();
          event.preventDefault();
        }}
      >
        <div className="fine">
          <div>
            <img className="finetree" src={fine} />
          </div>
          <div className="finetext">Now I'm fine at {moist_default}.</div>
        </div>

        <div className="submit">
          <div className="inputsubmit">
            <label>Moisture : </label>
            <input
              className="input-field"
              type="number"
              value={moist_defaultgarden}
              onChange={(e) => {
                setMoist_defultgarden(e.target.value);
              }}
            />
          </div>

          <Button name="Submit" type="submit" />
        </div>
      </form>

      <div className="sprinkle">
        <div className="sprinkle1">
          <div className="sprinkleheader">
            <div>Sprinkle 1</div>
          </div>
          <div>
            <div>
              <h3>Auto Watering</h3>
              {buzzer === true || sunroof === false ? (
                <div className="group">
                  <FormGroup switch disabled>
                    <Input type="switch" disabled />
                  </FormGroup>
                </div>
              ) : (
                <div className="group">
                  <FormGroup switch>
                    <Input
                      type="switch"
                      checked={is_auto1}
                      onChange={(e) => {
                        //setIs_auto1(!is_auto1garden);
                        handleIs_auto1(e);
                      }}
                    />
                  </FormGroup>
                </div>
              )}
            </div>
            <div>
              <h3>Watering</h3>
              {buzzer === true || is_auto1 === true || sunroof === false ? (
                <div className="group">
                  <FormGroup switch disabled>
                    <Input type="switch" disabled />
                  </FormGroup>
                </div>
              ) : (
                <div className="group">
                  <FormGroup switch>
                    <Input
                      type="switch"
                      checked={is_activate1}
                      onChange={(e) => {
                        //setis_activate1(!is_activate1garden);
                        handleIs_activate1(e);
                      }}
                    />
                  </FormGroup>
                </div>
              )}
            </div>
          </div>
        </div>
        <div className="sprinkle2">
          <div className="sprinkleheader">
            <div>Sprinkle 2</div>
          </div>
          <div>
            <div>
              <h3>Auto Watering</h3>
              {buzzer === true || sunroof === false ? (
                <div className="group">
                  <FormGroup switch disabled>
                    <Input type="switch" disabled />
                  </FormGroup>
                </div>
              ) : (
                <div className="group">
                  <FormGroup switch>
                    <Input
                      type="switch"
                      checked={is_auto2}
                      onChange={(e) => {
                        //setIs_auto2(!is_auto2garden);
                        handleIs_auto2(e);
                      }}
                    />
                  </FormGroup>
                </div>
              )}
            </div>
            <div>
              <h3>Watering</h3>
              {buzzer === true || is_auto2 === true || sunroof === false ? (
                <div className="group">
                  <FormGroup switch disabled>
                    <Input type="switch" disabled />
                  </FormGroup>
                </div>
              ) : (
                <div className="group">
                  <FormGroup switch>
                    <Input
                      type="switch"
                      checked={is_activate2}
                      onChange={(e) => {
                        //setis_activate2(!is_activate2garden);
                        handleIs_activate2(e);
                      }}
                    />
                  </FormGroup>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      <div className="sound">
        <div>
          <div className="sprinkleheader">
            <div>Sound</div>
          </div>
          <div className="groupsound">
            <FormGroup switch>
              <Input
                type="switch"
                checked={buzzer}
                onChange={(e) => {
                  // setBuzzer(!buzzergarden);
                  handleBuzzer(e);
                }}
              />
            </FormGroup>
          </div>
        </div>
        <div>
          <div className="sprinkleheader">
            <div>Sunroof</div>
          </div>
          {buzzer === true ? (
            <div className="groupsound">
              <FormGroup switch disabled>
                <Input type="switch" disabled />
              </FormGroup>
            </div>
          ) : (
            <div className="groupsound">
              <FormGroup switch>
                <Input
                  type="switch"
                  checked={sunroof}
                  onChange={(e) => {
                    //setSunroof(!sunroofgarden);
                    handleSunroof(e);
                  }}
                />
              </FormGroup>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Card;
