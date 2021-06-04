import React from 'react'
import { Formik } from 'formik'
import { useParams } from "react-router";
import './index.css'
import $ from 'jquery'
import jQuery from 'jquery'
import ReactMarkdown from 'react-markdown'

import { getUserDetails, postNewPrefix, getGuildInfo, getGuildModInfo, getPersonInfo } from '../../utils/api'
import auditTypeDict from '../../utils/auditDict';


export function DashboardPage(props) {


    const [user, setUser] = React.useState(null)
    const [loading, setLoading] = React.useState(true)
    const [prefix, setPrefix] = React.useState("%")
    const [guildInfo, setGuildInfo] = React.useState({ info: { icon: "", name: "--", roles: [] }, channels: [{ name: "hi", id: 100000000 }] })
    const { guildID, page } = useParams()
    const [welcomeMsg, setWelcomeMsg] = React.useState("")
    const [modInfo, setModInfo] = React.useState({ warns: [], bans: [], logs: [] })
    const [personInfoDict, setPersonInfoDict] = React.useState(new Map())

    async function getDataFromDiscord(uID) {
        getPersonInfo(uID).then((d) => {
            console.log(`done! ${d}`)
            return d;
        })
    }

    const date = new Date()

    React.useEffect(() => {
        getUserDetails().then(({ data }) => {
            console.log(data)
            setUser(data)
            setLoading(false)
        }).catch((err) => {
            console.error(err)
            setLoading(false)
            // window.location = 'http://localhost:3001/api/auth/discord'
        })
        getGuildInfo(guildID).then(({ data }) => {
            setGuildInfo(data)
            console.log(guildInfo)
        })
        getGuildModInfo(guildID).then(({ data }) => {
            // const test = getDataFromDiscord(data.warns[0].offender)
            data.warns.forEach((warn) => {
                if (personInfoDict.get(warn.offender) == undefined || personInfoDict.get(warn.offender) == null) {
                    getPersonInfo(warn.offender).then(async (personInfo) => {
                        console.log(personInfo.data)
                        personInfoDict.set(warn.offender, personInfo.data)
                        setPersonInfoDict(personInfoDict)
                    })
                }
            })
            // data.logs.slice(0,26).forEach((log) => {
            // if (personInfoDict.get(log.user_id) == undefined || personInfoDict.get(log.user_id) == null) {
            //     getPersonInfo(log.user_id).then(async (personInfo) => {
            //         console.log(personInfo.data)
            //         personInfoDict.set(log.user_id, personInfo.data)
            //         // setPersonInfoDict(personInfoDict)
            //     })
            // }
            // })

            // data.logs.slice(0,26).forEach((log) => {
            // if (personInfoDict.get(log.target_id) == undefined || personInfoDict.get(log.target_id) == null) {
            //     getPersonInfo(log.target_id).then(async (personInfo) => {
            //         console.log(personInfo.data)
            //         personInfoDict.set(log.target_id, personInfo.data)
            //         // setPersonInfoDict(personInfoDict)
            //     })
            // }
            // })

            data.log_users.forEach((u) => {
                personInfoDict.set(u.id, u)
                setPersonInfoDict(personInfoDict)
            })
            console.log(personInfoDict)
            setModInfo(data)
            console.log(data)
        })
        const timer = setTimeout(() => {
            console.log(personInfoDict)
            var warnsEle = document.querySelectorAll(".warn")
            console.log(warnsEle)
            for (var i = 0; i < warnsEle.length; i++) {
                warnsEle[i].addEventListener('click', (e) => {
                    console.log('clicked!')
                    console.log(document.getElementById(`expandable-${e.currentTarget.id}`))
                    console.log(`expandable-${e.currentTarget.id}`)
                    console.log(e.currentTarget)
                    document.getElementById(`expandable-${e.currentTarget.id}`).classList.toggle('warn-desc-open')
                    // console.log($(`.expandale-${$(this).attr('id')}`).html())
                    // // const info = 
                    // $(`.expandale-${$(this).attr('id')}`).toggleClass('warn-desc-open')
                    // info.find('.expandable').toggleClass('warn-desc-open')
                })
                console.log(warnsEle[i])
            }
            console.log(personInfoDict)

            console.log('Init Sidebar...')
            $(".sidebar-dropdown > a").on('click', function () {
                console.log('clicked')
                $(".sidebar-submenu").slideUp(200);
                if (
                    $(this)
                        .parent()
                        .hasClass("active")
                ) {
                    $(".sidebar-dropdown").removeClass("active");
                    $(this)
                        .parent()
                        .removeClass("active");
                } else {
                    $(".sidebar-dropdown").removeClass("active");
                    $(this)
                        .next(".sidebar-submenu")
                        .slideDown(200);
                    $(this)
                        .parent()
                        .addClass("active");
                }
            });

            $("#close-sidebar").on('click', function () {
                $(".page-wrapper").removeClass("toggled");
            });
            $("#show-sidebar").on('click', function () {
                $(".page-wrapper").addClass("toggled");
            });
            ; (function ($, window, document, undefined) {

                'use strict';

                var $html = $('html');

                $html.on('click.ui.dropdown', '.js-dropdown', function (e) {
                    e.preventDefault();
                    $(this).toggleClass('is-open');
                });

                $html.on('click.ui.dropdown', '.js-dropdown [data-dropdown-value]', function (e) {
                    e.preventDefault();
                    var $item = $(this);
                    var $dropdown = $item.parents('.js-dropdown');
                    $dropdown.find('.js-dropdown__input').val($item.data('dropdown-value'));
                    $dropdown.find('.js-dropdown__current').text($item.text());
                });

                $html.on('click.ui.dropdown', function (e) {
                    var $target = $(e.target);
                    if (!$target.parents().hasClass('js-dropdown')) {
                        $('.js-dropdown').removeClass('is-open');
                    }
                });

            })(jQuery, window, document);
        }, 1500)
        return () => {
            clearTimeout(timer)
        }
    }, [])



    // sidebarScript()

    return !loading && (
        //         <div>
        //             <div className="sidenav">
        //   <a href="#">About</a>
        //   <a href="#">Services</a>
        //   <a href="#">Clients</a>
        //   <a href="#">Contact</a>
        // </div>
        // <div className="main">
        // <h1>Dashboard Page</h1>
        //             <Formik initialValues={{ prefix: prefix }} onSubmit={(values) => { console.log(values); postNewPrefix(guildID, values.prefix) }}>
        //                 {
        //                     (props) => (
        //                         <form onSubmit={props.handleSubmit}>
        //                             <input type="text" name="prefix" onChange={props.handleChange} defaultValue={prefix} />
        //                             <button type="submit">Submit</button>
        //                         </form>
        //                     )
        //                 }
        //             </Formik>
        //         </div>
        // </div>
        <div className="page-wrapper chiller-theme toggled">
            <a id="show-sidebar" className="btn btn-sm btn-dark" href="#">
                <i className="fas fa-bars"></i>
            </a>
            <nav id="sidebar" className="sidebar-wrapper">
                <div className="sidebar-content">
                    <div className="sidebar-brand">
                        <a href="#">InfiniBot</a>
                        <div id="close-sidebar">
                            <i className="fas fa-times"></i>
                        </div>
                    </div>
                    <div className="sidebar-header">
                        <div className="user-pic">
                            <img className="img-responsive img-rounded" src={`https://cdn.discordapp.com/icons/${guildID}/${guildInfo.info.icon}.jpg`} alt="User picture" />
                        </div>
                        <div className="user-info">
                            <span className="user-name">{guildInfo.info.name}
                            </span>
                            <span className="user-role"><a href="../menu" style={{ color: `#818896` }}>	&#60; BACK</a></span>
                            {/* <span className="user-status">
            <i className="fa fa-circle"></i>
            <span>Online</span>
          </span> */}
                        </div>
                    </div>
                    <div className="sidebar-search">
                        <div>
                            <div className="input-group">
                                <input type="text" className="form-control search-menu" placeholder="Search..." />
                                <div className="input-group-append">
                                    <span className="input-group-text">
                                        <i className="fa fa-search" aria-hidden="true"></i>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="sidebar-menu">
                        <ul>
                            <li className="header-menu">
                                <span>General</span>
                            </li>
                            <li className="sidebar-dropdown">
                                <a href="#">
                                    <i className="fa fa-cog"></i>
                                    <span>Configuration</span>
                                    {/* <span className="badge badge-pill badge-warning">New</span> */}
                                </a>
                                <div className="sidebar-submenu">
                                    <ul>
                                        <li>
                                            <a href="./config#general">General
                    {/* <span className="badge badge-pill badge-success">Pro</span> */}
                                            </a>
                                        </li>
                                        <li>
                                            <a href="./config#welcome">Welcome</a>
                                        </li>
                                        <li>
                                            <a href="./config#logging">Logging</a>
                                        </li>
                                        <li>
                                            <a href="./config#misc">Miscellaneous</a>
                                        </li>
                                    </ul>
                                </div>
                            </li>
                            <li className="sidebar-dropdown">
                                <a href="#">
                                    <i className="fa fa-gavel"></i>
                                    <span>Moderation</span>
                                    {/* <span className="badge badge-pill badge-danger">3</span> */}
                                </a>
                                <div className="sidebar-submenu">
                                    <ul>
                                        <li>
                                            <a href="./moderation#warns">Warns</a>
                                        </li>
                                        <li>
                                            <a href="./moderation#bans">Bans</a>
                                        </li>
                                        <li>
                                            <a href="./moderation#logs">Moderation Log</a>
                                        </li>
                                    </ul>
                                </div>
                            </li>
                            <li className="sidebar-dropdown">
                                <a href="#">
                                    <i className="fas fa-chart-bar"></i>
                                    <span>Statistics</span>
                                </a>
                                <div className="sidebar-submenu">
                                    <ul>
                                        <li>
                                            <a href="./stats#general">General</a>
                                        </li>
                                        <li>
                                            <a href="./stats#messages">Messages</a>
                                        </li>
                                        <li>
                                            <a href="./stats#vc">Voice Channels</a>
                                        </li>
                                        <li>
                                            <a href="./stats#typing">Typing</a>
                                        </li>
                                        <li>
                                            <a href="./stats#leveling">Leveling</a>
                                        </li>
                                    </ul>
                                </div>
                            </li>

                            <li className="header-menu">
                                <span>Extra</span>
                            </li>
                            <li>
                                <a href="#">
                                    <i className="fa fa-book"></i>
                                    <span>Documentation</span>
                                    {/* <span className="badge badge-pill badge-primary">Beta</span> */}
                                </a>
                            </li>
                            <li>
                                <a href="#">
                                    <i className="fa fa-heartbeat"></i>
                                    <span>Status</span>
                                </a>
                            </li>
                            <li>
                                <a href="#">
                                    <i className="fa fa-ticket-alt"></i>
                                    <span>Support</span>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
                {/* <div className="sidebar-footer">
      <a href="#">
        <i className="fa fa-bell"></i>
        <span className="badge badge-pill badge-warning notification">3</span>
      </a>
      <a href="#">
        <i className="fa fa-envelope"></i>
        <span className="badge badge-pill badge-success notification">7</span>
      </a>
      <a href="#">
        <i className="fa fa-cog"></i>
        <span className="badge-sonar"></span>
      </a>
      <a href="#">
        <i className="fa fa-power-off"></i>
      </a>
    </div> */}
            </nav>
            <main className="page-content">
                <div className="container">

                    {/* <h1>Dashboard Page</h1>
                    <Formik initialValues={{ prefix: prefix }} onSubmit={(values) => { console.log(values); postNewPrefix(guildID, values.prefix) }}>
                        {
                            (props) => (
                                <form onSubmit={props.handleSubmit}>
                                    <input type="text" name="prefix" onChange={props.handleChange} defaultValue={prefix} />
                                    <button type="submit">Submit</button>
                                </form>
                            )
                        }
                    </Formik> */}
                    {
                        page == 'config' ? (
                            <div className="card-row">

                                <div className="col-sm-12 col-md-6">
                                    <div className="card">
                                        <header className="card-header">
                                            <div><i className="icon-settings">
                                            </i> General</div>
                                        </header>
                                        <div className="card-body">
                                            <fieldset className="form-group" id="__BVID__130">
                                                <div tabIndex="-1" role="group">
                                                    <h4 className="smalltitle">Custom Prefix</h4>
                                                    <p>Set the prefix you use to call commands</p>
                                                    <div role="group" className="input-group pb-1">
                                                        <input type="text" placeholder="Enter a prefix" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" defaultValue={prefix} />
                                                        <div className="input-group-append">
                                                        </div>
                                                    </div>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>

                                    <div className="card">
                                        <header className="card-header">
                                            <div><i className="icon-settings">
                                            </i> Logging</div>
                                        </header>
                                        <div className="card-body">
                                            <fieldset className="form-group" id="__BVID__130">
                                                <div tabIndex="-1" role="group">
                                                    <h4 className="smalltitle">Logging</h4>
                                                    <p>Get instant messages when something happens in your server for better moderation and managment!</p>
                                                    {/* <div role="group" className="input-group pb-1">
                                                        <input type="text" placeholder="Enter a prefix" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" defaultValue={prefix} />
                                                        <div className="input-group-append">
                                                        </div>
                                                    </div> */}
                                                    <h5>Have Logging Enabled</h5>
                                                    <div className="toggle">
                                                        <input type="checkbox" id="toggle" />
                                                        <label htmlFor="toggle"></label>
                                                    </div>
                                                    <h5>Choose Logging Channel</h5>
                                                    <div role="group" className="input-group pb-1">
                                                        {/* <input type="text" placeholder="Enter a prefix" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" value={prefix} />
                                                    <div className="input-group-append">
                                                    </div> */}
                                                        <div className="c-dropdown js-dropdown">
                                                            <input type="hidden" name="Framework" id="Framework" className="js-dropdown__input" />
                                                            <span className="c-button c-button--dropdown js-dropdown__current">Select Channel</span>
                                                            <ul className="c-dropdown__list">
                                                                {
                                                                    guildInfo.channels.map((channel) => (
                                                                        <li className="c-dropdown__item" data-dropdown-value={channel.id.toString()}>{channel.name}</li>
                                                                    )
                                                                    )
                                                                }
                                                                {/* <li className="c-dropdown__item" data-dropdown-value="angular">Angular</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="backbone">Backbone</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="ember">Ember</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="knockout">Knockout</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="react">React</li> */}
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>
                                    <div className="card">
                                        <header className="card-header">
                                            <div><i className="icon-settings">
                                            </i> Miscellaneous</div>
                                        </header>
                                        <div className="card-body">
                                            <fieldset className="form-group" id="__BVID__130">
                                                <div tabIndex="-1" role="group">
                                                    <h4 className="smalltitle">Miscellaneous</h4>
                                                    <p>Get instant messages when something happens in your server for better moderation and managment!</p>
                                                    {/* <div role="group" className="input-group pb-1">
                                                        <input type="text" placeholder="Enter a prefix" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" defaultValue={prefix} />
                                                        <div className="input-group-append">
                                                        </div>
                                                    </div> */}
                                                    <h5>Minecraft IP</h5>
                                                    <div role="group" className="input-group pb-1">
                                                        <input type="text" placeholder="play.mc.com or 192.xx.xx.xxx" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" />
                                                        <div className="input-group-append">
                                                        </div>
                                                    </div><br />
                                                    <h5>Choose Star Channel</h5>
                                                    <div role="group" className="input-group pb-1">
                                                        {/* <input type="text" placeholder="Enter a prefix" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" value={prefix} />
                                                    <div className="input-group-append">
                                                    </div> */}
                                                        <div className="c-dropdown js-dropdown">
                                                            <input type="hidden" name="Framework" id="Framework" className="js-dropdown__input" />
                                                            <span className="c-button c-button--dropdown js-dropdown__current">Select Channel</span>
                                                            <ul className="c-dropdown__list">
                                                                {
                                                                    guildInfo.channels.map((channel) => (
                                                                        <li className="c-dropdown__item" data-dropdown-value={channel.id.toString()}>{channel.name}</li>
                                                                    )
                                                                    )
                                                                }
                                                                {/* <li className="c-dropdown__item" data-dropdown-value="angular">Angular</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="backbone">Backbone</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="ember">Ember</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="knockout">Knockout</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="react">React</li> */}
                                                            </ul>
                                                        </div>
                                                    </div>
                                                    <br />
                                                    <h5>Welcome Nick</h5>
                                                    <div role="group" className="input-group pb-1">
                                                        <input type="text" placeholder="Enter a Welcome Nickname" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" defaultValue={prefix} />
                                                        <div className="input-group-append">
                                                        </div>
                                                    </div>
                                                    <br />
                                                    <h5>Welcome Role</h5>
                                                    <div role="group" className="input-group pb-1">
                                                        {/* <input type="text" placeholder="Enter a prefix" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" value={prefix} />
                                                    <div className="input-group-append">
                                                    </div> */}
                                                        <div className="c-dropdown js-dropdown">
                                                            <input type="hidden" name="Framework" id="Framework" className="js-dropdown__input" />
                                                            <span className="c-button c-button--dropdown js-dropdown__current">Select Role</span>
                                                            <ul className="c-dropdown__list">
                                                                {
                                                                    guildInfo.info.roles.map((role) => (
                                                                        <li className="c-dropdown__item" data-dropdown-value={role.id.toString()}>{role.name}</li>
                                                                    )
                                                                    )
                                                                }
                                                                {/* <li className="c-dropdown__item" data-dropdown-value="angular">Angular</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="backbone">Backbone</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="ember">Ember</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="knockout">Knockout</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="react">React</li> */}
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>
                                </div>
                                <div className="col-sm-12 col-md-6">
                                    <div className="card">
                                        <header className="card-header">
                                            <div><i className="icon-settings">
                                            </i> Welcome</div>
                                        </header>
                                        <div className="card-body">
                                            <fieldset className="form-group" id="__BVID__130">
                                                <div tabIndex="-1" role="group">
                                                    <h4 className="smalltitle">Welcome</h4>
                                                    Send a message when a new person joins your server! <br /> <br />
                                                Useful variables: <br />
                                                    <code>{`{member}`}</code>
                                                 - Mentions the person joining/leaving. <br />
                                                    <code>{`{members}`}</code>
                                                  - The number to members in the server <br />
                                                    <code>{`{user}`}</code>
                                                   - The person joining/leaving's name in the 'Wumpus#4201' format. <br />
                                                    <code>{`{guild}`}</code>
                                                    - The server name.
                                                    <br /> <br />
                                                    <h5>Welcome Channel
                                                    </h5>
                                                    <div role="group" className="input-group pb-1">
                                                        {/* <input type="text" placeholder="Enter a prefix" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" value={prefix} />
                                                    <div className="input-group-append">
                                                    </div> */}
                                                        <div className="c-dropdown js-dropdown">
                                                            <input type="hidden" name="Framework" id="Framework" className="js-dropdown__input" />
                                                            <span className="c-button c-button--dropdown js-dropdown__current">Select Welcome Channel</span>
                                                            <ul className="c-dropdown__list">
                                                                {
                                                                    guildInfo.channels.map((channel) => (
                                                                        <li className="c-dropdown__item" data-dropdown-value={channel.id.toString()}>{channel.name}</li>
                                                                    )
                                                                    )
                                                                }
                                                                {/* <li className="c-dropdown__item" data-dropdown-value="angular">Angular</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="backbone">Backbone</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="ember">Ember</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="knockout">Knockout</li>
                                                            <li className="c-dropdown__item" data-dropdown-value="react">React</li> */}
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </div>

                                            </fieldset>
                                            <fieldset>
                                                <br />
                                                <h5>Welcome Message</h5>
                                                <textarea placeholder="Hey {member}, welcome to {guild}!" rows="6" wrap="soft" className="col-12 form-control welcomeMsg" maxLength="5000" type="text" id="__BVID__332" spellCheck="true" onChange={(value) => setWelcomeMsg(value.target.value)}></textarea>
                                                <br />
                                                <h5>Welcome Message Preview</h5>
                                                <div className="wrapper">
                                                    <div className="side-colored"></div>
                                                    <div className="card-embed embed">
                                                        <div className="card-block">
                                                            <div className="embed-inner"><div className="embed-author"><img className="embed-author-icon" src="https://cdn.discordapp.com/avatars/645388150524608523/c58a466d4d44f14ea1470860f61d64a6.webp?size=256" /><a className="embed-author-name" href="">{`{user} just joined the server!`}</a></div><div className="embed-description"><ReactMarkdown>{welcomeMsg}</ReactMarkdown></div></div>
                                                        </div>
                                                        {/* <div className="embed-footer"><span>{(date.getMonth() + 1) + '/' + date.getDate() + '/' + date.getFullYear()}</span></div> */}
                                                    </div>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>
                                </div>


                            </div>
                        ) : page == 'moderation' ? (
                            <div className="card-row">

                                <div className="col-sm-12 col-md-6">
                                    <div className="card">
                                        <header className="card-header">
                                            <div><i className="icon-settings">
                                            </i> Warns</div>
                                        </header>
                                        <div className="card-body">
                                            <fieldset className="form-group" id="__BVID__130">
                                                <div tabIndex="-1" role="group">
                                                    <h4 className="smalltitle">Warns</h4>
                                                    <p>The following players have been warned, you can change the reason, revoke, or add a warn by pressing the designated buttons</p>
                                                    <div role="group" className="input-group pb-1">
                                                        <input type="text" placeholder="Enter a prefix" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" defaultValue={prefix} />
                                                        <div className="input-group-append">
                                                            <button type="button" className="btn btn-primary">Warn</button>
                                                        </div>
                                                    </div>
                                                    <div className="warnList">
                                                        {/* <div className="warn">
                                                            <div className="warnInfo">
                                                                <p>User#6969</p>
                                                                <p className="modText">Moderator: kidsonfilms:4635</p>
                                                                <p className="modText">4/12/21</p>
                                                                <div className="expandable">
                                                                <p>reasonreasonreasonreasonreasonreasonreasonreasonreasonreason</p>
                                                            </div>
                                                            </div>
                                                            <div className="warnActions">
                                                            {/* <i className="fas fa-edit fa-lg"></i>
                                                            <i className="fas fa-ban fa-lg"></i>
                                                            </div> */}

                                                        {
                                                            modInfo.warns.map((warn) => (
                                                                <div className="warn" id={`warn-${warn._id}`}>
                                                                    <div className="warnInfo">
                                                                        <p>{warn.name}#{personInfoDict.get(warn.offender) != undefined ? personInfoDict.get(warn.offender).discriminator : ''} <span className="modText">uID: {warn.offender}</span></p>
                                                                        <p className="modText">Moderator: {personInfoDict.get(warn.mod) != undefined ? personInfoDict.get(warn.mod).username + '#' + personInfoDict.get(warn.mod).discriminator : '--'}</p>
                                                                        <p className="modText">{warn.time}</p>
                                                                        <div className="expandable" id={`expandable-warn-${warn._id}`}>
                                                                            <p>{warn.reason}</p>
                                                                        </div>
                                                                    </div>
                                                                    <div className="warnActions">
                                                                        {/* <i className="fas fa-edit fa-lg"></i>*/}
                                                                        <i className="fas fa-ban fa-lg"></i>
                                                                    </div>
                                                                </div>
                                                            ))
                                                        }
                                                    </div>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>

                                    <div className="card">
                                        <header className="card-header">
                                            <div><i className="icon-settings">
                                            </i> Logs</div>
                                        </header>
                                        <div className="card-body">
                                            <fieldset className="form-group" id="__BVID__130">
                                                <div tabIndex="-1" role="group">
                                                    <h4 className="smalltitle">Moderation Log</h4>
                                                    <p>Get instant messages when something happens in your server for better moderation and managment!</p>
                                                    {/* <div role="group" className="input-group pb-1">
                                                    <input type="text" placeholder="Enter a prefix" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" defaultValue={prefix} />
                                                    <div className="input-group-append">
                                                    </div>
                                                </div> */}
                                                    <div className="warnList">

                                                        {
                                                            modInfo.logs.slice(0,26).map((log) => (
                                                                <div className="warn" id={`log-${log.id}`}>
                                                                    <div className="warnInfo">
                                                                        <p>{auditTypeDict.get(log.action_type)} <span class="modText">CODE {log.action_type}</span></p>
                                                                        <p className="modText">Target: {personInfoDict.get(log.target_id) != undefined ? personInfoDict.get(log.target_id).username + '#' + personInfoDict.get(log.target_id).discriminator : '--'}</p>
                                                                        <p className="modText">Moderator: {personInfoDict.get(log.user_id) != undefined ? personInfoDict.get(log.user_id).username + '#' + personInfoDict.get(log.user_id).discriminator : '--'}</p>
                                                                        {/* <p className="modText">4/11/12</p> */}
                                                                        <div className="expandable" id={`expandable-log-${log.id}`}>
                                                                            <p>{log.action}</p>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            ))
                                                        }
                                                    </div>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>
                                </div>
                                <div className="col-sm-12 col-md-6">
                                    <div className="card">
                                        <header className="card-header">
                                            <div><i className="icon-settings">
                                            </i> Bans</div>
                                        </header>
                                        <div className="card-body">
                                            <fieldset className="form-group" id="__BVID__130">
                                                <div tabIndex="-1" role="group">
                                                    <h4 className="smalltitle">Bans </h4>
                                                    <p>The following players have been banned, you can change the reason, revoke, or add a ban by pressing the designated buttons</p>
                                                    <div role="group" className="input-group pb-1">
                                                        <input type="text" placeholder="Enter a prefix" className="col-12 form-control" pattern=".{1,50}" maxLength="50" id="__BVID__131" defaultValue={prefix} />
                                                        <div className="input-group-append">
                                                            <button type="button" className="btn btn-primary">Warn</button>
                                                        </div>
                                                    </div>
                                                    <div className="warnList">

                                                        {
                                                            modInfo.bans.map((ban) => (
                                                                <div className="warn" id={`ban-${ban.user.id}`}>
                                                                    <div className="warnInfo">
                                                                        <p>{ban.user.username}#{ban.user.discriminator}</p>
                                                                        <p className="modText">uID: {ban.user.id}</p>
                                                                        {/* <p className="modText">Moderator: kidsonfilms</p>
                                                                        <p className="modText">4/11/12</p> */}
                                                                        <div className="expandable" id={`expandable-ban-${ban.user.id}`}>
                                                                            <p>{ban.reason}</p>
                                                                        </div>
                                                                    </div>
                                                                    <div className="warnActions">
                                                                        {/* <i className="fas fa-edit fa-lg"></i>*/}
                                                                        <i className="fas fa-ban fa-lg"></i>
                                                                    </div>
                                                                </div>
                                                            ))
                                                        }
                                                    </div>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>
                                </div>


                            </div>) : page == 'stats' ? (<h1>Statistics</h1>) : (<h1>404</h1>)
                    }



                </div>

            </main>
        </div>
    )
}