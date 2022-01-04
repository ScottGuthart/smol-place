from flask import render_template, flash, url_for, request, redirect
from app.models import Site
from app.main import bp
from app import db
from app.main.forms import AddSiteForm


@bp.route("/")
def index():
    return redirect(url_for("main.add_alias"))


@bp.route("/add", methods=["GET", "POST"])
def add_alias():
    form = AddSiteForm()
    if form.validate_on_submit():
        site = Site(url=form.url.data, alias=form.alias.data)
        db.session.add(site)
        db.session.commit()
        flash(
            "Your smol url is:"
            f" {url_for('main.alias_redirect', alias=form.alias.data, _external=True)}"
        )
        return redirect(url_for("main.add_alias"))
    return render_template("add_alias.html", title="Shorten URL", form=form)


@bp.route("/<alias>", methods=["GET"])
def alias_redirect(alias):
    site = Site.query.filter(Site.alias.ilike(alias)).first_or_404()
    return redirect(site.url)
