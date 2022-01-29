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
        ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
        site = Site(url=form.url.data, alias=form.alias.data, ip=ip)
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
    if site.visits is None:
        site.visits = 0
    site.visits += 1
    db.session.commit()
    return redirect(site.url)
