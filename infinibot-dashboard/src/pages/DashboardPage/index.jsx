import React from 'react'
import { Link } from 'react'
import { Formik } from 'formik'
import { useParams } from "react-router";
import './index.css'
import sidebarScript from './sidebar'
import $ from 'jquery'
import jQuery from 'jquery'
import MDEditor from "@uiw/react-md-editor";
import ReactMarkdown from 'react-markdown'

import { getUserDetails, postNewPrefix, getGuildInfo } from '../../utils/api'


export function DashboardPage(props) {


    const [user, setUser] = React.useState(null)
    const [loading, setLoading] = React.useState(true)
    const [prefix, setPrefix] = React.useState("%")
    const [guildInfo, setGuildInfo] = React.useState({ info: { icon: "", name: "--", roles: [] }, channels: [{ name: "hi", id: 100000000 }] })
    const { guildID, page } = useParams()
    const [welcomeMsg, setWelcomeMsg] = React.useState()

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
        const timer = setTimeout(() => {
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
        }, 1000)
        return () => {
            clearTimeout(timer)
        }
    }, [])



    // sidebarScript()

    return !loading && (
        //         <div>
        //             <div class="sidenav">
        //   <a href="#">About</a>
        //   <a href="#">Services</a>
        //   <a href="#">Clients</a>
        //   <a href="#">Contact</a>
        // </div>
        // <div class="main">
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
        <div class="page-wrapper chiller-theme toggled">
            <a id="show-sidebar" class="btn btn-sm btn-dark" href="#">
                <i class="fas fa-bars"></i>
            </a>
            <nav id="sidebar" class="sidebar-wrapper">
                <div class="sidebar-content">
                    <div class="sidebar-brand">
                        <a href="#">InfiniBot</a>
                        <div id="close-sidebar">
                            <i class="fas fa-times"></i>
                        </div>
                    </div>
                    <div class="sidebar-header">
                        <div class="user-pic">
                            <img class="img-responsive img-rounded" src={`https://cdn.discordapp.com/icons/${guildID}/${guildInfo.info.icon}.jpg`} alt="User picture" />
                        </div>
                        <div class="user-info">
                            <span class="user-name">{guildInfo.info.name}
                            </span>
                            <span class="user-role"><a href="../menu" style={{ color: `#818896` }}>	&#60; BACK</a></span>
                            {/* <span class="user-status">
            <i class="fa fa-circle"></i>
            <span>Online</span>
          </span> */}
                        </div>
                    </div>
                    <div class="sidebar-search">
                        <div>
                            <div class="input-group">
                                <input type="text" class="form-control search-menu" placeholder="Search..." />
                                <div class="input-group-append">
                                    <span class="input-group-text">
                                        <i class="fa fa-search" aria-hidden="true"></i>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="sidebar-menu">
                        <ul>
                            <li class="header-menu">
                                <span>General</span>
                            </li>
                            <li class="sidebar-dropdown">
                                <a href="#">
                                    <i class="fa fa-cog"></i>
                                    <span>Configuration</span>
                                    {/* <span class="badge badge-pill badge-warning">New</span> */}
                                </a>
                                <div class="sidebar-submenu">
                                    <ul>
                                        <li>
                                            <a href="#">General
                    {/* <span class="badge badge-pill badge-success">Pro</span> */}
                                            </a>
                                        </li>
                                        <li>
                                            <a href="#">Welcome</a>
                                        </li>
                                        <li>
                                            <a href="#">Logging</a>
                                        </li>
                                        <li>
                                            <a href="#">Miscellaneous</a>
                                        </li>
                                    </ul>
                                </div>
                            </li>
                            <li class="sidebar-dropdown">
                                <a href="#">
                                    <i class="fa fa-gavel"></i>
                                    <span>Moderation</span>
                                    {/* <span class="badge badge-pill badge-danger">3</span> */}
                                </a>
                                <div class="sidebar-submenu">
                                    <ul>
                                        <li>
                                            <a href="#">Warns</a>
                                        </li>
                                        <li>
                                            <a href="#">Bans</a>
                                        </li>
                                        <li>
                                            <a href="#">Moderation Log</a>
                                        </li>
                                    </ul>
                                </div>
                            </li>
                            <li class="sidebar-dropdown">
                                <a href="#">
                                    <i class="fas fa-chart-bar"></i>
                                    <span>Statistics</span>
                                </a>
                                <div class="sidebar-submenu">
                                    <ul>
                                        <li>
                                            <a href="#">General</a>
                                        </li>
                                        <li>
                                            <a href="#">Messages</a>
                                        </li>
                                        <li>
                                            <a href="#">Voice Channels</a>
                                        </li>
                                        <li>
                                            <a href="#">Typing</a>
                                        </li>
                                        <li>
                                            <a href="#">Leveling</a>
                                        </li>
                                    </ul>
                                </div>
                            </li>

                            <li class="header-menu">
                                <span>Extra</span>
                            </li>
                            <li>
                                <a href="#">
                                    <i class="fa fa-book"></i>
                                    <span>Documentation</span>
                                    {/* <span class="badge badge-pill badge-primary">Beta</span> */}
                                </a>
                            </li>
                            <li>
                                <a href="#">
                                    <i class="fa fa-heartbeat"></i>
                                    <span>Status</span>
                                </a>
                            </li>
                            <li>
                                <a href="#">
                                    <i class="fa fa-ticket-alt"></i>
                                    <span>Support</span>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
                {/* <div class="sidebar-footer">
      <a href="#">
        <i class="fa fa-bell"></i>
        <span class="badge badge-pill badge-warning notification">3</span>
      </a>
      <a href="#">
        <i class="fa fa-envelope"></i>
        <span class="badge badge-pill badge-success notification">7</span>
      </a>
      <a href="#">
        <i class="fa fa-cog"></i>
        <span class="badge-sonar"></span>
      </a>
      <a href="#">
        <i class="fa fa-power-off"></i>
      </a>
    </div> */}
            </nav>
            <main class="page-content">
                <div class="container">

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
                            <div class="card-row">

                                <div class="col-sm-12 col-md-6">
                                    <div class="card">
                                        <header class="card-header">
                                            <div><i class="icon-settings">
                                            </i> General</div>
                                        </header>
                                        <div class="card-body">
                                            <fieldset class="form-group" id="__BVID__130">
                                                <div tabindex="-1" role="group">
                                                    <h4 class="smalltitle">Custom Prefix</h4>
                                                    <p>Set the prefix you use to call commands</p>
                                                    <div role="group" class="input-group pb-1">
                                                        <input type="text" placeholder="Enter a prefix" class="col-12 form-control" pattern=".{1,50}" maxlength="50" id="__BVID__131" defaultValue={prefix} />
                                                        <div class="input-group-append">
                                                        </div>
                                                    </div>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>

                                    <div class="card">
                                        <header class="card-header">
                                            <div><i class="icon-settings">
                                            </i> Logging</div>
                                        </header>
                                        <div class="card-body">
                                            <fieldset class="form-group" id="__BVID__130">
                                                <div tabindex="-1" role="group">
                                                    <h4 class="smalltitle">Logging</h4>
                                                    <p>Get instant messages when something happens in your server for better moderation and managment!</p>
                                                    {/* <div role="group" class="input-group pb-1">
                                                        <input type="text" placeholder="Enter a prefix" class="col-12 form-control" pattern=".{1,50}" maxlength="50" id="__BVID__131" defaultValue={prefix} />
                                                        <div class="input-group-append">
                                                        </div>
                                                    </div> */}
                                                    <h5>Have Logging Enabled</h5>
                                                    <div class="toggle">
                                                        <input type="checkbox" id="toggle" />
                                                        <label for="toggle"></label>
                                                    </div>
                                                    <h5>Choose Logging Channel</h5>
                                                    <div role="group" class="input-group pb-1">
                                                        {/* <input type="text" placeholder="Enter a prefix" class="col-12 form-control" pattern=".{1,50}" maxlength="50" id="__BVID__131" value={prefix} />
                                                    <div class="input-group-append">
                                                    </div> */}
                                                        <div class="c-dropdown js-dropdown">
                                                            <input type="hidden" name="Framework" id="Framework" class="js-dropdown__input" />
                                                            <span class="c-button c-button--dropdown js-dropdown__current">Select Channel</span>
                                                            <ul class="c-dropdown__list">
                                                                {
                                                                    guildInfo.channels.map((channel) => (
                                                                        <li class="c-dropdown__item" data-dropdown-value={channel.id.toString()}>{channel.name}</li>
                                                                    )
                                                                    )
                                                                }
                                                                {/* <li class="c-dropdown__item" data-dropdown-value="angular">Angular</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="backbone">Backbone</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="ember">Ember</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="knockout">Knockout</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="react">React</li> */}
                                                            </ul>
                                                        </div> 
                                                        </div>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>
                                    <div class="card">
                                        <header class="card-header">
                                            <div><i class="icon-settings">
                                            </i> Miscellaneous</div>
                                        </header>
                                        <div class="card-body">
                                            <fieldset class="form-group" id="__BVID__130">
                                                <div tabindex="-1" role="group">
                                                    <h4 class="smalltitle">Miscellaneous</h4>
                                                    <p>Get instant messages when something happens in your server for better moderation and managment!</p>
                                                    {/* <div role="group" class="input-group pb-1">
                                                        <input type="text" placeholder="Enter a prefix" class="col-12 form-control" pattern=".{1,50}" maxlength="50" id="__BVID__131" defaultValue={prefix} />
                                                        <div class="input-group-append">
                                                        </div>
                                                    </div> */}
                                                    <h5>Minecraft IP</h5>
                                                    <div role="group" class="input-group pb-1">
                                                        <input type="text" placeholder="play.mc.com or 192.xx.xx.xxx" class="col-12 form-control" pattern=".{1,50}" maxlength="50" id="__BVID__131" />
                                                        <div class="input-group-append">
                                                        </div>
                                                    </div><br/>
                                                    <h5>Choose Star Channel</h5>
                                                    <div role="group" class="input-group pb-1">
                                                        {/* <input type="text" placeholder="Enter a prefix" class="col-12 form-control" pattern=".{1,50}" maxlength="50" id="__BVID__131" value={prefix} />
                                                    <div class="input-group-append">
                                                    </div> */}
                                                        <div class="c-dropdown js-dropdown">
                                                            <input type="hidden" name="Framework" id="Framework" class="js-dropdown__input" />
                                                            <span class="c-button c-button--dropdown js-dropdown__current">Select Channel</span>
                                                            <ul class="c-dropdown__list">
                                                                {
                                                                    guildInfo.channels.map((channel) => (
                                                                        <li class="c-dropdown__item" data-dropdown-value={channel.id.toString()}>{channel.name}</li>
                                                                    )
                                                                    )
                                                                }
                                                                {/* <li class="c-dropdown__item" data-dropdown-value="angular">Angular</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="backbone">Backbone</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="ember">Ember</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="knockout">Knockout</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="react">React</li> */}
                                                            </ul>
                                                        </div> 
                                                        </div>
                                                        <br/>
                                                        <h5>Welcome Nick</h5>
                                                        <div role="group" class="input-group pb-1">
                                                        <input type="text" placeholder="Enter a Welcome Nickname" class="col-12 form-control" pattern=".{1,50}" maxlength="50" id="__BVID__131" defaultValue={prefix} />
                                                        <div class="input-group-append">
                                                        </div>
                                                    </div>
                                                    <br/>
                                                    <h5>Welcome Role</h5>
                                                    <div role="group" class="input-group pb-1">
                                                        {/* <input type="text" placeholder="Enter a prefix" class="col-12 form-control" pattern=".{1,50}" maxlength="50" id="__BVID__131" value={prefix} />
                                                    <div class="input-group-append">
                                                    </div> */}
                                                        <div class="c-dropdown js-dropdown">
                                                            <input type="hidden" name="Framework" id="Framework" class="js-dropdown__input" />
                                                            <span class="c-button c-button--dropdown js-dropdown__current">Select Role</span>
                                                            <ul class="c-dropdown__list">
                                                                {
                                                                    guildInfo.info.roles.map((role) => (
                                                                        <li class="c-dropdown__item" data-dropdown-value={role.id.toString()}>{role.name}</li>
                                                                    )
                                                                    )
                                                                }
                                                                {/* <li class="c-dropdown__item" data-dropdown-value="angular">Angular</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="backbone">Backbone</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="ember">Ember</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="knockout">Knockout</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="react">React</li> */}
                                                            </ul>
                                                        </div> 
                                                        </div>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-sm-12 col-md-6">
                                    <div class="card">
                                        <header class="card-header">
                                            <div><i class="icon-settings">
                                            </i> Welcome</div>
                                        </header>
                                        <div class="card-body">
                                            <fieldset class="form-group" id="__BVID__130">
                                                <div tabindex="-1" role="group">
                                                    <h4 class="smalltitle">Welcome</h4>
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
                                                    <div role="group" class="input-group pb-1">
                                                        {/* <input type="text" placeholder="Enter a prefix" class="col-12 form-control" pattern=".{1,50}" maxlength="50" id="__BVID__131" value={prefix} />
                                                    <div class="input-group-append">
                                                    </div> */}
                                                        <div class="c-dropdown js-dropdown">
                                                            <input type="hidden" name="Framework" id="Framework" class="js-dropdown__input" />
                                                            <span class="c-button c-button--dropdown js-dropdown__current">Select Welcome Channel</span>
                                                            <ul class="c-dropdown__list">
                                                                {
                                                                    guildInfo.channels.map((channel) => (
                                                                        <li class="c-dropdown__item" data-dropdown-value={channel.id.toString()}>{channel.name}</li>
                                                                    )
                                                                    )
                                                                }
                                                                {/* <li class="c-dropdown__item" data-dropdown-value="angular">Angular</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="backbone">Backbone</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="ember">Ember</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="knockout">Knockout</li>
                                                            <li class="c-dropdown__item" data-dropdown-value="react">React</li> */}
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </div>

                                            </fieldset>
                                            <fieldset>
                                                <br />
                                                <h5>Welcome Message</h5>
                                                <textarea placeholder="Hey {member}, welcome to {guild}!" rows="6" wrap="soft" class="col-12 form-control welcomeMsg" maxlength="5000" type="text" id="__BVID__332" spellcheck="true" onChange={(value) => setWelcomeMsg(value.target.value)}></textarea>
                                                <br />
                                                <h5>Welcome Message Preview</h5>
                                                <div class="wrapper">
                                                    <div class="side-colored"></div>
                                                    <div class="card-embed embed">
                                                        <div class="card-block">
                                                            <div class="embed-inner"><div class="embed-author"><img class="embed-author-icon" src="https://cdn.discordapp.com/avatars/645388150524608523/c58a466d4d44f14ea1470860f61d64a6.webp?size=256" /><a class="embed-author-name" href="">{`{user} just joined the server!`}</a></div><div class="embed-description"><ReactMarkdown>{welcomeMsg}</ReactMarkdown></div></div>
                                                        </div>
                                                        {/* <div class="embed-footer"><span>{(date.getMonth() + 1) + '/' + date.getDate() + '/' + date.getFullYear()}</span></div> */}
                                                    </div>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>
                                </div>


                            </div>
                        ) : page == 'moderation' ? (<h1>Moderation</h1>) : page == 'stats' ? (<h1>Statistics</h1>) : (<h1>404</h1>)
                    }



                </div>

            </main>
        </div>
    )
}